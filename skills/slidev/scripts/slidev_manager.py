#!/usr/bin/env python3
"""
Slidev Presentation Manager
Main script for managing Slidev presentations.
"""

import os
import subprocess
import sys
import json
from pathlib import Path
from typing import Optional, List, Dict, Any


class SlidevManager:
    """Manager for Slidev presentation operations."""
    
    def __init__(self, project_path: Optional[str] = None):
        self.project_path = Path(project_path) if project_path else Path.cwd()
        self.slides_file = self.project_path / "slides.md"
        self.package_file = self.project_path / "package.json"
    
    def is_slidev_project(self) -> bool:
        """Check if current directory is a Slidev project."""
        return self.slides_file.exists() or self.package_file.exists()
    
    def find_slidev_projects(self, search_path: Optional[str] = None) -> List[Path]:
        """Find all Slidev projects in given path."""
        search_dir = Path(search_path) if search_path else Path.cwd()
        projects = []
        
        for root, dirs, files in os.walk(search_dir):
            if "slides.md" in files or "package.json" in files:
                projects.append(Path(root))
        
        return projects
    
    def create_project(self, name: str, theme: str = "default") -> Dict[str, Any]:
        """Create a new Slidev project."""
        project_dir = self.project_path / name
        
        if project_dir.exists():
            return {
                "success": False,
                "error": f"Directory {name} already exists"
            }
        
        try:
            project_dir.mkdir(parents=True)
            os.chdir(project_dir)
            
            # Create package.json
            package_content = {
                "name": name,
                "type": "module",
                "private": True,
                "scripts": {
                    "dev": "slidev --open",
                    "build": "slidev build",
                    "export": "slidev export"
                },
                "dependencies": {
                    "@slidev/cli": "latest",
                    "@slidev/theme-default": "latest"
                },
                "devDependencies": {
                    "playwright-chromium": "latest"
                }
            }
            
            with open("package.json", "w", encoding="utf-8") as f:
                json.dump(package_content, f, indent=2)
            
            # Create slides.md with template
            slides_content = f'''---
theme: {theme}
title: {name.replace("-", " ").title()}
---

# {name.replace("-", " ").title()}

Presentation subtitle

---

# What is Slidev?

Slidev is a slide deck maker and presenter designed for developers:

- 📝 **Text-based** - Focus on content with Markdown
- 🎨 **Themable** - Themes can be shared via npm
- 🧑‍💻 **Developer Friendly** - Code highlighting, live coding
- 🎥 **Recording** - Built-in recording and camera view
- 📤 **Portable** - Export to PDF, PNG, or SPA

---

# Code Highlighting

```python
def hello():
    print("Hello, Slidev!")
```

---

# Thank You!

Questions?
'''
            
            with open("slides.md", "w", encoding="utf-8") as f:
                f.write(slides_content)
            
            # Create README.md
            readme_content = f'''# {name.replace("-", " ").title()}

A Slidev presentation.

## Getting Started

```bash
# Install dependencies
pnpm install

# Start dev server
pnpm dev

# Export to PDF
pnpm export

# Build static site
pnpm build
```

## Resources

- [Slidev Docs](https://sli.dev/)
- [Syntax Guide](https://sli.dev/guide/syntax)
'''
            
            with open("README.md", "w", encoding="utf-8") as f:
                f.write(readme_content)
            
            return {
                "success": True,
                "project_path": str(project_dir.absolute()),
                "message": f"Project '{name}' created successfully!"
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def start_dev_server(self, port: Optional[int] = None, open_browser: bool = True) -> Dict[str, Any]:
        """Start Slidev development server."""
        if not self.is_slidev_project():
            return {
                "success": False,
                "error": "No Slidev project found in current directory"
            }
        
        try:
            cmd = ["slidev"]
            if port:
                cmd.extend(["--port", str(port)])
            if open_browser:
                cmd.append("--open")
            
            subprocess.Popen(cmd, cwd=self.project_path)
            
            return {
                "success": True,
                "message": f"Dev server starting on port {port or 'default'}"
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def export_slides(self, 
                      format_type: str = "pdf",
                      output: Optional[str] = None,
                      with_clicks: bool = False,
                      dark: bool = False,
                      range_str: Optional[str] = None,
                      wait: Optional[int] = None) -> Dict[str, Any]:
        """Export slides to various formats."""
        if not self.is_slidev_project():
            return {
                "success": False,
                "error": "No Slidev project found in current directory"
            }
        
        try:
            cmd = ["slidev", "export"]
            
            if format_type != "pdf":
                cmd.extend(["--format", format_type])
            if output:
                cmd.extend(["--output", output])
            if with_clicks:
                cmd.append("--with-clicks")
            if dark:
                cmd.append("--dark")
            if range_str:
                cmd.extend(["--range", range_str])
            if wait:
                cmd.extend(["--wait", str(wait)])
            
            result = subprocess.run(cmd, cwd=self.project_path, capture_output=True, text=True)
            
            if result.returncode == 0:
                return {
                    "success": True,
                    "message": f"Exported successfully to {format_type.upper()}",
                    "output": result.stdout
                }
            else:
                return {
                    "success": False,
                    "error": result.stderr
                }
                
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def build(self, base: Optional[str] = None) -> Dict[str, Any]:
        """Build static site for hosting."""
        if not self.is_slidev_project():
            return {
                "success": False,
                "error": "No Slidev project found in current directory"
            }
        
        try:
            cmd = ["slidev", "build"]
            if base:
                cmd.extend(["--base", base])
            
            result = subprocess.run(cmd, cwd=self.project_path, capture_output=True, text=True)
            
            if result.returncode == 0:
                return {
                    "success": True,
                    "message": "Build completed successfully! Check the 'dist' folder.",
                    "output": result.stdout
                }
            else:
                return {
                    "success": False,
                    "error": result.stderr
                }
                
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def format_slides(self) -> Dict[str, Any]:
        """Format slides.md file."""
        if not self.slides_file.exists():
            return {
                "success": False,
                "error": "slides.md not found"
            }
        
        try:
            result = subprocess.run(
                ["slidev", "format"],
                cwd=self.project_path,
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                return {
                    "success": True,
                    "message": "Slides formatted successfully!"
                }
            else:
                return {
                    "success": False,
                    "error": result.stderr
                }
                
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def get_slide_info(self) -> Dict[str, Any]:
        """Get information about current slides."""
        if not self.slides_file.exists():
            return {
                "success": False,
                "error": "slides.md not found"
            }
        
        try:
            with open(self.slides_file, "r", encoding="utf-8") as f:
                content = f.read()
            
            # Count slides (separated by ---)
            slides = content.split("---")
            
            # Extract headmatter if exists
            headmatter = {}
            if slides and slides[0].strip().startswith("theme:") or "title:" in slides[0]:
                import yaml
                try:
                    headmatter = yaml.safe_load(slides[0])
                except:
                    pass
            
            return {
                "success": True,
                "slide_count": len([s for s in slides if s.strip()]),
                "headmatter": headmatter,
                "file_size": len(content),
                "file_path": str(self.slides_file)
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }


def main():
    """Main entry point for CLI usage."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Slidev Presentation Manager")
    subparsers = parser.add_subparsers(dest="command", help="Commands")
    
    # Create command
    create_parser = subparsers.add_parser("create", help="Create new project")
    create_parser.add_argument("name", help="Project name")
    create_parser.add_argument("--theme", default="default", help="Theme name")
    
    # Dev command
    dev_parser = subparsers.add_parser("dev", help="Start dev server")
    dev_parser.add_argument("--port", type=int, help="Port number")
    
    # Export command
    export_parser = subparsers.add_parser("export", help="Export slides")
    export_parser.add_argument("--format", default="pdf", choices=["pdf", "pptx", "png", "md"])
    export_parser.add_argument("--output", help="Output filename")
    export_parser.add_argument("--with-clicks", action="store_true", help="Export with click animations")
    export_parser.add_argument("--dark", action="store_true", help="Export in dark mode")
    export_parser.add_argument("--range", help="Slide range to export (e.g., 1,3-5,7)")
    
    # Build command
    build_parser = subparsers.add_parser("build", help="Build static site")
    build_parser.add_argument("--base", help="Base URL")
    
    # Format command
    subparsers.add_parser("format", help="Format slides")
    
    # Info command
    subparsers.add_parser("info", help="Get slide info")
    
    args = parser.parse_args()
    
    manager = SlidevManager()
    
    if args.command == "create":
        result = manager.create_project(args.name, args.theme)
    elif args.command == "dev":
        result = manager.start_dev_server(args.port)
    elif args.command == "export":
        result = manager.export_slides(
            args.format,
            args.output,
            args.with_clicks,
            args.dark,
            args.range
        )
    elif args.command == "build":
        result = manager.build(args.base)
    elif args.command == "format":
        result = manager.format_slides()
    elif args.command == "info":
        result = manager.get_slide_info()
    else:
        parser.print_help()
        sys.exit(1)
    
    print(json.dumps(result, indent=2, ensure_ascii=False))
    sys.exit(0 if result.get("success") else 1)


if __name__ == "__main__":
    main()
