"""Mobile web development tools."""

import json
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..core.file_operations import FileOperations


class MobileTools:
    """Tools for mobile web development."""

    def __init__(self, file_ops: "FileOperations"):
        self.file_ops = file_ops

    def create_pwa_manifest(self, app_name: str, description: str = "Mobile Web Application") -> str:
        """Create PWA manifest.json file."""
        manifest = {
            "name": app_name,
            "short_name": app_name,
            "description": description,
            "start_url": "/",
            "display": "standalone",
            "background_color": "#0ea5e9",
            "theme_color": "#0ea5e9",
            "orientation": "portrait-primary",
            "icons": [
                {
                    "src": "/icon-192x192.png",
                    "sizes": "192x192",
                    "type": "image/png"
                },
                {
                    "src": "/icon-512x512.png",
                    "sizes": "512x512",
                    "type": "image/png"
                }
            ]
        }

        content = json.dumps(manifest, indent=2)
        return self.file_ops.write_file("public/manifest.json", content)

    def create_service_worker(self) -> str:
        """Create basic service worker for PWA."""
        sw_content = """
// Service Worker for Mobile Web App PWA
const CACHE_NAME = 'mobile-app-v1';
const urlsToCache = [
  '/',
  '/static/js/bundle.js',
  '/static/css/main.css',
  '/manifest.json'
];

self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then(cache => cache.addAll(urlsToCache))
  );
});

self.addEventListener('fetch', event => {
  event.respondWith(
    caches.match(event.request)
      .then(response => {
        if (response) {
          return response;
        }
        return fetch(event.request);
      })
  );
});
"""
        return self.file_ops.write_file("public/sw.js", sw_content.strip())

    def create_responsive_component(self, component_name: str, props: str = "") -> str:
        """Create a responsive React component template."""
        component_content = f"""
import React from 'react';

interface {component_name}Props {{
  {props}
}}

const {component_name}: React.FC<{component_name}Props> = (props) => {{
  return (
    <div className="w-full max-w-md mx-auto p-4 sm:max-w-lg md:max-w-xl lg:max-w-2xl">
      <div className="bg-white rounded-lg shadow-md p-6">
        <h2 className="text-xl font-bold text-gray-900 mb-4">
          {component_name}
        </h2>
        {{/* Component content here */}}
      </div>
    </div>
  );
}};

export default {component_name};
"""
        return self.file_ops.write_file(f"src/components/{component_name}.tsx", component_content.strip())

    def setup_tailwind(self) -> str:
        """Set up Tailwind CSS for the project."""
        # Tailwind config
        config_content = """
/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/**/*.{js,jsx,ts,tsx}",
    "./public/index.html"
  ],
  theme: {
    extend: {
      colors: {
        'primary': '#0ea5e9',
        'secondary': '#14b8a6',
        'accent': '#fbbf24'
      }
    },
  },
  plugins: [],
}
"""
        result1 = self.file_ops.write_file("tailwind.config.js", config_content.strip())

        # CSS file
        css_content = """
@tailwind base;
@tailwind components;
@tailwind utilities;

@layer base {
  body {
    @apply font-sans antialiased;
  }
}

@layer components {
  .btn-primary {
    @apply bg-primary hover:bg-blue-600 text-white font-bold py-2 px-4 rounded-lg transition-colors;
  }

  .card {
    @apply bg-white rounded-lg shadow-md p-6 border border-gray-200;
  }
}
"""
        result2 = self.file_ops.write_file("src/index.css", css_content.strip())

        return f"{result1}\\n{result2}"

    def create_mobile_layout(self, layout_name: str) -> str:
        """Create mobile-first layout component."""
        layout_content = f"""
import React from 'react';

interface {layout_name}Props {{
  children: React.ReactNode;
  title?: string;
}}

const {layout_name}: React.FC<{layout_name}Props> = ({{ children, title }}) => {{
  return (
    <div className="min-h-screen bg-gray-50">
      {{/* Mobile Header */}}
      <header className="bg-primary text-white p-4 sticky top-0 z-10">
        <div className="flex items-center justify-between">
          <h1 className="text-lg font-bold">{{title || 'Mobile App'}}</h1>
          <button className="p-2 hover:bg-blue-600 rounded">
            <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={{2}} d="M4 6h16M4 12h16M4 18h16" />
            </svg>
          </button>
        </div>
      </header>

      {{/* Main Content */}}
      <main className="pb-16 sm:pb-0">
        {{children}}
      </main>

      {{/* Mobile Bottom Navigation */}}
      <nav className="fixed bottom-0 left-0 right-0 bg-white border-t border-gray-200 sm:hidden">
        <div className="grid grid-cols-4 py-2">
          <button className="flex flex-col items-center p-2 text-primary">
            <span className="text-xs mt-1">Home</span>
          </button>
          <button className="flex flex-col items-center p-2 text-gray-600">
            <span className="text-xs mt-1">Features</span>
          </button>
          <button className="flex flex-col items-center p-2 text-gray-600">
            <span className="text-xs mt-1">Settings</span>
          </button>
          <button className="flex flex-col items-center p-2 text-gray-600">
            <span className="text-xs mt-1">Profile</span>
          </button>
        </div>
      </nav>
    </div>
  );
}};

export default {layout_name};
"""
        return self.file_ops.write_file(f"src/components/{layout_name}.tsx", layout_content.strip())

    def test_mobile_responsive(self) -> str:
        """Test mobile responsiveness using Lighthouse."""
        return self.file_ops.run_bash("npx lighthouse --only-categories=performance,accessibility --form-factor=mobile --chrome-flags='--headless' http://localhost:3000")