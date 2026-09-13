import { Moon, Sun } from 'lucide-react';
import { useTheme } from '../context/ThemeContext';
import { haptic } from '../lib/telegram';

export function ThemeToggle() {
  const { theme, toggleTheme } = useTheme();

  return (
    <button
      className="p-1.5 ml-1 text-neutral-600 dark:text-neutral-300 hover:bg-neutral-100 dark:hover:bg-neutral-800 rounded-md transition-colors"
      onClick={() => {
        haptic('light');
        toggleTheme();
      }}
      title="Toggle Theme"
      aria-label="Toggle Theme"
    >
      {theme === 'dark' ? <Moon size={18} /> : <Sun size={18} />}
    </button>
  );
}
