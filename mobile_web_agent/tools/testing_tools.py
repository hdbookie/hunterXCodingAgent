"""Testing framework tools."""

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..core.file_operations import FileOperations


class TestingTools:
    """Tools for setting up and running tests."""

    def __init__(self, file_ops: "FileOperations"):
        self.file_ops = file_ops

    def setup_jest(self) -> str:
        """Set up Jest testing framework."""
        jest_config = """
module.exports = {
  testEnvironment: 'jsdom',
  setupFilesAfterEnv: ['<rootDir>/src/setupTests.ts'],
  moduleNameMapping: {
    '\\\\.(css|less|scss|sass)$': 'identity-obj-proxy',
  },
  testMatch: [
    '<rootDir>/src/**/__tests__/**/*.{js,jsx,ts,tsx}',
    '<rootDir>/src/**/*.{spec,test}.{js,jsx,ts,tsx}'
  ],
  collectCoverageFrom: [
    'src/**/*.{js,jsx,ts,tsx}',
    '!src/**/*.d.ts',
    '!src/index.tsx'
  ],
  coverageThreshold: {
    global: {
      branches: 70,
      functions: 70,
      lines: 70,
      statements: 70
    }
  }
};
"""

        setup_tests = """
import '@testing-library/jest-dom';
"""

        result1 = self.file_ops.write_file("jest.config.js", jest_config.strip())
        result2 = self.file_ops.write_file("src/setupTests.ts", setup_tests.strip())

        return f"{result1}\\n{result2}"

    def setup_playwright(self) -> str:
        """Set up Playwright for E2E testing."""
        playwright_config = """
import { defineConfig, devices } from '@playwright/test';

export default defineConfig({
  testDir: './tests/e2e',
  fullyParallel: true,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 2 : 0,
  workers: process.env.CI ? 1 : undefined,
  reporter: 'html',
  use: {
    baseURL: 'http://localhost:3000',
    trace: 'on-first-retry',
  },

  projects: [
    {
      name: 'chromium',
      use: { ...devices['Desktop Chrome'] },
    },
    {
      name: 'Mobile Chrome',
      use: { ...devices['Pixel 5'] },
    },
    {
      name: 'Mobile Safari',
      use: { ...devices['iPhone 12'] },
    },
  ],

  webServer: {
    command: 'npm start',
    url: 'http://localhost:3000',
    reuseExistingServer: !process.env.CI,
  },
});
"""
        return self.file_ops.write_file("playwright.config.ts", playwright_config.strip())

    def create_unit_tests(self, component_name: str) -> str:
        """Create unit tests for a component."""
        test_content = f"""
import React from 'react';
import {{ render, screen, fireEvent }} from '@testing-library/react';
import {component_name} from '../{component_name}';

describe('{component_name}', () => {{
  it('renders without crashing', () => {{
    render(<{component_name} />);
    expect(screen.getByText('{component_name}')).toBeInTheDocument();
  }});

  it('handles user interactions correctly', () => {{
    render(<{component_name} />);
    // Add specific interaction tests here
  }});

  it('displays correct data when props are provided', () => {{
    const testProps = {{
      // Add test props here
    }};
    render(<{component_name} {{...testProps}} />);
    // Add assertions here
  }});
}});
"""
        return self.file_ops.write_file(f"src/components/__tests__/{component_name}.test.tsx", test_content.strip())

    def create_integration_tests(self) -> str:
        """Create integration tests."""
        test_content = """
import React from 'react';
import { render, screen, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import App from '../App';

describe('App Integration Tests', () => {
  it('navigates between pages correctly', async () => {
    const user = userEvent.setup();
    render(<App />);

    // Test navigation flow
    expect(screen.getByText('Mobile App')).toBeInTheDocument();

    // Add more integration test scenarios
  });

  it('handles form submissions correctly', async () => {
    const user = userEvent.setup();
    render(<App />);

    // Test form interactions
    // Add form testing logic
  });
});
"""
        return self.file_ops.write_file("src/__tests__/App.integration.test.tsx", test_content.strip())

    def create_e2e_tests(self) -> str:
        """Create end-to-end tests with Playwright."""
        e2e_content = """
import { test, expect } from '@playwright/test';

test.describe('Mobile App E2E Tests', () => {
  test('mobile navigation works correctly', async ({ page }) => {
    await page.goto('/');

    // Test mobile responsive behavior
    await page.setViewportSize({ width: 375, height: 812 });

    await expect(page.getByText('Mobile App')).toBeVisible();

    // Test bottom navigation
    await page.getByText('Features').click();
    await expect(page).toHaveURL(/.*features/);
  });

  test('user flow completion', async ({ page }) => {
    await page.goto('/');

    // Add complete user flow tests here
    await expect(page.getByText('Mobile App')).toBeVisible();
  });
});
"""
        return self.file_ops.write_file("tests/e2e/mobile-app.spec.ts", e2e_content.strip())

    def run_all_tests(self) -> str:
        """Run all test suites."""
        results = []

        # Run unit tests
        results.append("=== UNIT TESTS ===")
        results.append(self.file_ops.run_bash("npm test -- --coverage --watchAll=false"))

        # Run E2E tests
        results.append("\\n=== E2E TESTS ===")
        results.append(self.file_ops.run_bash("npx playwright test"))

        return "\\n".join(results)

    def test_mobile_performance(self) -> str:
        """Test mobile performance using Lighthouse."""
        return self.file_ops.run_bash("npx lighthouse --only-categories=performance --form-factor=mobile --output=json --output-path=./lighthouse-mobile.json http://localhost:3000")