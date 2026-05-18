#!/usr/local/bin/pythoncipeo

from autopkglib import Processor, ProcessorError

__all__ = ["VersionSanitizer"]

class VersionSanitizer(Processor):
    """Replaces invalid characters in version strings."""
    
    input_variables = {
        "version": {
            "required": True,
            "description": "Version string to sanitize.",
        }
    }
    output_variables = {
        "version": {
            "description": "Sanitized version string.",
        }
    }

    def main(self):
        original = self.env["version"]
        sanitized = original.replace("+", ".")
        self.env["version"] = sanitized
        self.output(f"Version sanitized: {original} → {sanitized}")

if __name__ == "__main__":
    PROCESSOR = VersionSanitizer()
    PROCESSOR.execute_shell()