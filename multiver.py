#!/usr/bin/env python3

from dataclasses import dataclass
from pathlib import Path
from typing import Optional, Tuple
import logging
import platform
import getpass
import sys
from tkinter import TclError
import ttkbootstrap as tb
from ttkbootstrap.constants import *
import distro
from PIL import ImageTk, Image

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@dataclass
class SystemInfo:
    """Data class to store system information."""
    os_name: str
    os_version: str
    username: str
    build_number: Optional[str] = None
    
    def __str__(self) -> str:
        """Return a formatted string of system information."""
        info = f"{self.os_name} {self.os_version}"
        if self.build_number:
            info += f" (Build {self.build_number})"
        return info

class SystemInfoCollector:
    """Handles gathering system information across different platforms."""
    
    @staticmethod
    def get_system_info() -> SystemInfo:
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
                raise NotImplementedError(f"Unsupported operating system: {system}")
                
        except Exception as e:
            logger.error(f"Error collecting system information: {e}")
            raise

class BannerManager:
    """Handles loading and managing system banners."""
    
    def __init__(self, base_path: Path):
        self.base_path = base_path / "banner"
        self.default_width = 400
        self.default_height = 180
        
    def get_banner_path(self, system_info: SystemInfo) -> Path:
        """Get the appropriate banner path for the current system."""
        try:
            if "macOS" in system_info.os_name:
                banner_dir = self.base_path / "macOS" / str(int(float(system_info.os_version.split('.')[0])))
            elif "Linux" in system_info.os_name:
                banner_dir = self.base_path / "linux" / distro.id()
            else:
                raise ValueError(f"Unsupported OS for banner: {system_info.os_name}")

            # Check for both PNG and JPG
            for ext in ['.png', '.jpg']:
                if (banner_dir.with_suffix(ext)).exists():
                    return banner_dir.with_suffix(ext)
                    
            # If no specific banner found, use default
            return self._get_default_banner()
            
        except Exception as e:
            logger.warning(f"Error loading banner: {e}, using default")
            return self._get_default_banner()
    
    def _get_default_banner(self) -> Path:
        """Return path to default banner."""
        default_banner = self.base_path / "default.png"
        if not default_banner.exists():
            raise FileNotFoundError("Default banner not found")
        return default_banner
    
    def load_banner(self, path: Path, width: int, height: int) -> ImageTk.PhotoImage:
        """Load and resize banner image."""
        try:
            img = Image.open(path).resize((width, height))
            return ImageTk.PhotoImage(img)
        except Exception as e:
            logger.error(f"Error loading banner image: {e}")
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
        self.root.geometry(f"{self.width}x{self.height}")
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
            logger.error(f"Error creating banner: {e}")
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
        text = f"""
        {str(self.system_info)}
        
        Copyright to respective owners above. All rights reserved.

        The {self.system_info.os_name} operating system may come with a warranty or it may not. Just depends on what it is.

        This product, be it: the combination of software, hardware, and customizations are from the proud owner of this computer:
            {self.system_info.username}

        """
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
            logger.error(f"Failed to copy to clipboard: {e}")
            
    def run(self):
        """Start the application."""
        try:
            self.create_widgets()
            self.root.mainloop()
        except Exception as e:
            logger.error(f"Application error: {e}")
            raise

def main():
    """Main entry point for the application."""
    try:
        app = MultiverWindow()
        app.run()
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
