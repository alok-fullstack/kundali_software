'use client';

import React from 'react';

interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: 'primary' | 'secondary' | 'success' | 'muhurta' | 'health' | 'chat' | 'outline';
  size?: 'sm' | 'md' | 'lg';
  isLoading?: boolean;
  fullWidth?: boolean;
  children: React.ReactNode;
}

export function Button({
  variant = 'primary',
  size = 'md',
  isLoading = false,
  fullWidth = false,
  children,
  className = '',
  disabled,
  ...props
}: ButtonProps) {
  const baseStyles = 'font-semibold rounded-lg transition-all duration-200 focus:outline-none focus:ring-2 focus:ring-offset-2 disabled:cursor-not-allowed';

  const variantStyles = {
    primary: 'bg-gradient-primary text-white hover:scale-[1.02] focus:ring-primary-500 disabled:opacity-50 disabled:hover:scale-100',
    secondary: 'bg-secondary text-white hover:bg-secondary-light focus:ring-secondary disabled:opacity-50',
    success: 'bg-green-500 text-white hover:bg-green-600 focus:ring-green-500 disabled:opacity-50',
    muhurta: 'bg-gradient-muhurta text-white hover:scale-[1.02] focus:ring-purple-500 disabled:opacity-50 disabled:hover:scale-100',
    health: 'bg-gradient-health text-white hover:scale-[1.02] focus:ring-red-500 disabled:opacity-50 disabled:hover:scale-100',
    chat: 'bg-gradient-chat text-white hover:scale-[1.02] focus:ring-indigo-500 disabled:opacity-50 disabled:hover:scale-100',
    outline: 'border-2 border-primary-500 text-primary-500 hover:bg-primary-50 focus:ring-primary-500 disabled:opacity-50',
  };

  const sizeStyles = {
    sm: 'px-3 py-1.5 text-sm',
    md: 'px-5 py-2.5 text-base',
    lg: 'px-8 py-4 text-lg',
  };

  const widthStyle = fullWidth ? 'w-full' : '';

  return (
    <button
      className={`${baseStyles} ${variantStyles[variant]} ${sizeStyles[size]} ${widthStyle} ${className}`}
      disabled={disabled || isLoading}
      {...props}
    >
      {isLoading ? (
        <span className="flex items-center justify-center gap-2">
          <svg className="animate-spin h-5 w-5" viewBox="0 0 24 24">
            <circle
              className="opacity-25"
              cx="12"
              cy="12"
              r="10"
              stroke="currentColor"
              strokeWidth="4"
              fill="none"
            />
            <path
              className="opacity-75"
              fill="currentColor"
              d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
            />
          </svg>
          <span>लोड हो रहा है... / Loading...</span>
        </span>
      ) : (
        children
      )}
    </button>
  );
}
