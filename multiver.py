#!/usr/bin/env python3

import logging
import platform
import getpass
import sys
from tkinter import TclError
import ttkbootstrap as tb
from ttkbootstrap.constants import *
import distro
from PIL import ImageTk, Image
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class SystemInfo:
    """Data class to store system information."""
    def __init__(self, os_name, os_version, username, build_number=None):
        self.os_name = os_name
        self.os_version = os_version
        self.username = username
        self.build_number = build_number
    
    def __str__(self):
        """Return a formatted string of system information."""
        info = "{0} {1}".format(self.os_name, self.os_version)
        if self.build_number:
            info += " (Build {0})".format(self.build_number)
        return info

class SystemInfoCollector:
    """Handles gathering system information across different platforms."""
    
    @staticmethod
    def get_system_info():
        """Collect system information based on the current platform."""
        username = getpass.getuser()
        system = platform.system()
        
        try:
            if system == "Darwin":
                # macOS specific information
                build = platform.mac_ver()[0]
                return SystemInfo(
                    os_name="macOS",
                    os_version=platform.mac_ver()[0],
                    username=username,
                    build_number=platform.release()
                )
            elif system == "Linux":
                # Linux specific information
                version = distro.os_release_attr("version") or "rolling"
                return SystemInfo(
                    os_name=distro.name(pretty=True),
                    os_version=version,
                    username=username
                )
            elif system == "Windows":
                logger.info("Windows detected - this program is meant for Unix-like systems")
                sys.exit("Please use winver.exe instead")
            else:
                raise NotImplementedError("Unsupported operating system: {0}".format(system))
                
        except Exception as e:
            logger.error("Error collecting system information: {0}".format(e))
            raise

class BannerManager:
    """Handles loading and managing system banners."""
    
    def __init__(self, base_path):
        self.base_path = base_path / "banner"
        self.default_width = 400
        self.default_height = 180
        
    def get_banner_path(self, system_info):
        """Get the appropriate banner path for the current system."""
        try:
            if "macOS" in system_info.os_name:
                banner_dir = self.base_path / "macOS" / str(int(float(system_info.os_version.split('.')[0])))
            elif "Linux" in system_info.os_name:
                banner_dir = self.base_path / "linux" / distro.id()
            else:
                raise ValueError("Unsupported OS for banner: {0}".format(system_info.os_name))

            # Check for both PNG and JPG
            for ext in ['.png', '.jpg']:
                if (banner_dir.with_suffix(ext)).exists():
                    return banner_dir.with_suffix(ext)
                    
            # If no specific banner found, use default
            return self._get_default_banner()
            
        except Exception as e:
            logger.warning("Error loading banner: {0}, using default".format(e))
            return self._get_default_banner()
    
    def _get_default_banner(self):
        """Return path to default banner."""
        default_banner = self.base_path / "default.png"
        if not default_banner.exists():
            raise FileNotFoundError("Default banner not found")
        return default_banner
    
    def load_banner(self, path, width, height):
        """Load and resize banner image."""
        try:
            img = Image.open(path).resize((width, height))
            return ImageTk.PhotoImage(img)
        except Exception as e:
            logger.error("Error loading banner image: {0}".format(e))
            raise

class MultiverWindow:
    """Main application window class."""
    
    def __init__(self):
        self.width = 400
        self.height = 450
        self.system_info = SystemInfoCollector.get_system_info()
        self.banner_manager = BannerManager(Path(__file__).parent)
        
        # Initialize main window
        self.root = tb.Window(themename="cosmo")
        self.root.title("multiver.py")
        self.root.geometry("{0}x{1}".format(self.width, self.height))
        self.root.resizable(False, False)
        
        # Store references to prevent garbage collection
        self.banner_image = None
        
    def create_widgets(self):
        """Create and arrange all window widgets."""
        self._create_banner()
        self._create_separator()
        self._create_info_text()
        self._create_buttons()
        
    def _create_banner(self):
        """Create and display the banner image."""
        try:
            banner_path = self.banner_manager.get_banner_path(self.system_info)
            self.banner_image = self.banner_manager.load_banner(
                banner_path,
                self.width,
                int(self.height/2.5)
            )
            banner_label = tb.Label(self.root, image=self.banner_image)
            banner_label.pack()
        except Exception as e:
            logger.error("Error creating banner: {0}".format(e))
            # Create text-based header instead
            header = tb.Label(
                self.root,
                text=str(self.system_info),
                font=("Helvetica", 16, "bold")
            )
            header.pack(pady=20)
            
    def _create_separator(self):
        """Create separator between banner and text."""
        separator = tb.Separator(self.root, bootstyle="secondary", orient="horizontal")
        separator.pack(fill="x")
        
    def _create_info_text(self):
        """Create and display system information text."""
        text = """
        {0}
        
        Copyright to respective owners above. All rights reserved.

        The {1} operating system may come with a warranty or it may not. Just depends on what it is.

        This product, be it: the combination of software, hardware, and customizations are from the proud owner of this computer:
            {2}

        """.format(
            str(self.system_info),
            self.system_info.os_name,
            self.system_info.username
        )
        text_display = tb.Label(
            self.root,
            text=text,
            wraplength=self.width-20,
            justify="left"
        )
        text_display.pack(pady=20)
        
    def _create_buttons(self):
        """Create control buttons."""
        button_frame = tb.Frame(self.root)
        button_frame.pack(side="bottom", pady=20)
        
        # Copy Info button
        copy_btn = tb.Button(
            button_frame,
            text="Copy Info",
            bootstyle="secondary",
            command=self._copy_to_clipboard
        )
        copy_btn.pack(side="left", padx=5)
        
        # OK button
        ok_btn = tb.Button(
            button_frame,
            text="OK",
            bootstyle="primary",
            command=self.root.quit
        )
        ok_btn.pack(side="left", padx=5)
        
    def _copy_to_clipboard(self):
        """Copy system information to clipboard."""
        try:
            self.root.clipboard_clear()
            self.root.clipboard_append(str(self.system_info))
            self.root.update()
        except TclError as e:
            logger.error("Failed to copy to clipboard: {0}".format(e))
            
    def run(self):
        """Start the application."""
        try:
            self.create_widgets()
            self.root.mainloop()
        except Exception as e:
            logger.error("Application error: {0}".format(e))
            raise

def main():
    """Main entry point for the application."""
    try:
        app = MultiverWindow()
        app.run()
    except Exception as e:
        logger.error("Fatal error: {0}".format(e))
        sys.exit(1)

if __name__ == "__main__":
    main()
