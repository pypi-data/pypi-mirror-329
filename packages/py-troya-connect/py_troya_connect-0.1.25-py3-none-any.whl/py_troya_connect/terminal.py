import win32com.client
import pythoncom
import time
 
class ExtraTerminalError(Exception):
    """Base exception for ExtraTerminal errors."""
    pass
 
class ExtraTerminal:
    """
    A Python interface to interact with Attachmate Extra Terminal sessions via COM API.
    
    Args:
        session_name (str): Name of the Extra session to connect to.
    """
    
    def __init__(self, session_name):
        pythoncom.CoInitialize()
        self.timeout = 10000
        self.counter = 0
        try:
            self.extra_app = win32com.client.Dispatch("EXTRA.System")
            print(f"Successfully created EXTRA.System object: {self.extra_app}")
            
            # List available sessions first
            sessions = self.list_available_sessions()
            print(f"Available sessions: {sessions}")
            
            if not sessions:
                raise ExtraTerminalError("No sessions available")
            
            # Try to get session by index if session_name is numeric
            try:
                session_index = int(session_name)
                self.session = self.extra_app.Sessions(session_index)
            except ValueError:
                # If session_name is not numeric, try to find by name
                found = False
                for i in range(1, self.extra_app.Sessions.Count + 1):
                    session = self.extra_app.Sessions(i)
                    if session.Name == session_name:
                        self.session = session
                        found = True
                        break
                if not found:
                    raise ExtraTerminalError(f"Session '{session_name}' not found")
            
            print(f"Successfully connected to session: {self.session.Name}")
            self.screen = self.session.Screen
            self.connected = True
            
        except Exception as e:
            print(f"Initialization error: {str(e)}")
            raise ExtraTerminalError(f"Failed to initialize: {str(e)}") from e

    def list_available_sessions(self):
        """List all available Extra terminal sessions"""
        try:
            sessions = []
            for i in range(1, self.extra_app.Sessions.Count + 1):
                session = self.extra_app.Sessions(i)
                sessions.append({
                    'index': i,
                    'name': session.Name,
                    'connected': session.Connected
                })
            return sessions
        except pythoncom.com_error as e:
            return f"Failed to list sessions: {self._format_com_error(e)}"

    def _format_com_error(self, error):
        """Format COM error details for better diagnosis"""
        hr, msg, exc, arg = error.args
        return f"Code: {hr}, Message: {msg}, Source: {exc}, Param: {arg}"

    def check_system_status(self):
        """Diagnostic method to check system status"""
        try:
            versions = {
                'Extra Version': self.extra_app.Version,
                'Session Count': self.extra_app.Sessions.Count,
                'Available Sessions': [sess.Name for sess in self.extra_app.Sessions]
            }
            return versions
        except pythoncom.com_error as e:
            return f"Failed to get system status: {self._format_com_error(e)}"

    def connect(self):
        """Connect to the Extra terminal session."""
        if not self.connected:
            try:
                self.session.Connect()
                self.connected = True
            except pythoncom.com_error as e:
                raise ExtraTerminalError(f"Connection failed: {e}") from e
 
    def disconnect(self):
        """Safe disconnect handling"""
        try:
            if hasattr(self, 'connected') and self.connected:
                self.connected = False
        except Exception as e:
            print(f"Disconnect warning: {str(e)}")

    def is_connected(self):
        """Check if the session is connected."""
        return self.session.Connected
 
    def send_keys(self, keys):
        """
        Send keystrokes to the terminal.
        
        Args:
            keys (str): Keys to send (supports special keys like {ENTER}, {TAB}).
        """
        if not self.is_connected():
            raise ExtraTerminalError("Not connected to terminal")
        try:
            self.screen.SendKeys(keys)
        except pythoncom.com_error as e:
            raise ExtraTerminalError(f"SendKeys failed: {e}") from e
 
    def read_screen(self):
        """Read the entire terminal screen using GetStringEx"""
        try:
            # Use 24x80 as default terminal size
            response = self.screen.GetStringEx(0, 0, 24, 80, 120, 0, 0, 0)
            response = response[:1920]  # 24 rows * 80 columns
            screen_text = []
            for i in range(0, len(response), 80):
                line = response[i:i+80].rstrip()
                screen_text.append(line)
            return screen_text
        except Exception as e:
            raise ExtraTerminalError(f"Read screen failed: {str(e)}") from e
 
    def wait_for_text(self, text, timeout=30, interval=0.5):
        """Wait until specified text appears on the screen."""
        start_time = time.time()
        while time.time() - start_time < timeout:
            try:
                screen_text = self.read_screen()
                for line in screen_text:
                    if text in line:
                        return True
                # Check OIA status
                if hasattr(self.screen, 'OIA') and self.screen.OIA.XStatus != 0:
                    self.counter += 1
                    if self.counter > self.timeout:
                        return False
            except Exception:
                pass
            time.sleep(interval)
        return False
 
    def get_cursor_position(self):
        """
        Get current cursor position (row, column).
        
        Returns:
            tuple: (row, column) coordinates.
        """
        if not self.is_connected():
            raise ExtraTerminalError("Not connected to terminal")
        try:
            # Using correct property names for Attachmate Extra API
            return (self.screen.CurrentRow, self.screen.CurrentColumn)
        except pythoncom.com_error as e:
            raise ExtraTerminalError(f"Cursor position failed: {e}") from e
        except AttributeError:
            # Fallback for older versions or different configurations
            try:
                cursor = self.screen.OIA.CursorPosition
                return (cursor.Row, cursor.Column)
            except Exception as e:
                raise ExtraTerminalError(f"Cursor position not available: {str(e)}") from e
 
    @staticmethod
    def select_session():
        """Interactive method to select a session"""
        try:
            # Create temporary instance just to list sessions
            temp_app = win32com.client.Dispatch("EXTRA.System")
            sessions = []
            
            print("\nAvailable Sessions:")
            print("------------------")
            
            for i in range(1, temp_app.Sessions.Count + 1):
                session = temp_app.Sessions(i)
                sessions.append({
                    'index': i,
                    'name': session.Name,
                    'connected': session.Connected
                })
                status = "Connected" if session.Connected else "Disconnected"
                print(f"{i}. {session.Name} ({status})")
            
            while True:
                choice = input("\nSelect session (enter number): ").strip()
                try:
                    session_index = int(choice)
                    if 1 <= session_index <= len(sessions):
                        return str(session_index)
                    else:
                        print("Invalid session number. Please try again.")
                except ValueError:
                    print("Please enter a valid number.")
                    
        except Exception as e:
            print(f"Error listing sessions: {str(e)}")
            return "1"  # Default to first session if error occurs

    def format_command(self, command):
        """Format command with proper terminal key entries"""
        # If command already contains formatted keys, return as is
        if any(key in command for key in ['<ENTER>', '<TAB>', '<CLEAR>', '<PA1>', '<PA2>', '<PA3>', '<RESET>']):
            return command

        # Replace common commands with their terminal equivalents
        replacements = {
            '{ENTER}': '<ENTER>',
            '{TAB}': '<TAB>',
            '{CLEAR}': '<CLEAR>',
            '{PA1}': '<PA1>',
            '{PA2}': '<PA2>',
            '{PA3}': '<PA3>',
            '{RESET}': '<RESET>'
        }
        
        result = command.strip()
        
        # Apply replacements
        for old, new in replacements.items():
            if old in result:
                result = result.replace(old, new)
                return result  # Return immediately if a replacement was made
        
        # If no special keys were found, add <ENTER>
        return result + ' <ENTER>'

    def send_command(self, command):
        """Send formatted command to terminal"""
        formatted_command = self.format_command(command)
        print(f"Sending formatted command: {formatted_command}")
        self.send_keys(formatted_command)
        return formatted_command

    def __enter__(self):
        self.connect()
        return self
 
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.disconnect()
        try:
            pythoncom.CoUninitialize()
        except Exception as e:
            print(f"CoUninitialize warning: {str(e)}")
 
# Example Usage
if __name__ == "__main__":
    try:
        print("Initializing Extra Terminal and selecting session...")
        
        # Get session selection from user
        session_choice = ExtraTerminal.select_session()
        
        # Connect to selected session and read screen
        with ExtraTerminal(session_choice) as terminal:
            print("\nConnected successfully!")
            print("\nReading current screen content:")
            print("-" * 80)
            
            screen_content = terminal.read_screen()
            for line in screen_content:
                if line.strip():  # Only print non-empty lines
                    print(line)
                    
            print("-" * 80)
            
    except ExtraTerminalError as e:
        print(f"Error: {e}")
    except KeyboardInterrupt:
        print("\nOperation cancelled by user.")

