'use client';

import { useMemo } from 'react';

interface AvatarProps {
  name?: string;
  picture?: string;
  size?: 'sm' | 'md' | 'lg';
}

const colors = [
  'bg-blue-500',
  'bg-green-500',
  'bg-purple-500',
  'bg-pink-500',
  'bg-indigo-500',
  'bg-red-500',
  'bg-yellow-500',
  'bg-teal-500',
];

export default function Avatar({ name, picture, size = 'md' }: AvatarProps) {
  const sizeClasses = {
    sm: 'w-8 h-8 text-sm',
    md: 'w-10 h-10 text-base',
    lg: 'w-16 h-16 text-2xl'
  };

  // Generate consistent color based on name
  const bgColor = useMemo(() => {
    if (!name) return colors[0];
    const hash = name.split('').reduce((acc, char) => acc + char.charCodeAt(0), 0);
    return colors[hash % colors.length];
  }, [name]);

  const initial = name?.charAt(0).toUpperCase() || 'U';

  return (
    <div className={`${sizeClasses[size]} rounded-full overflow-hidden flex items-center justify-center border-2 border-blue-500`}>
      {picture ? (
        <img
          src={picture}
          alt={name || 'User'}
          className="w-full h-full object-cover"
          onError={(e) => {
            // Hide image on error and show fallback
            e.currentTarget.style.display = 'none';
            if (e.currentTarget.nextElementSibling) {
              (e.currentTarget.nextElementSibling as HTMLElement).style.display = 'flex';
            }
          }}
        />
      ) : null}
      <div 
        className={`w-full h-full ${bgColor} flex items-center justify-center text-white font-semibold ${picture ? 'hidden' : 'flex'}`}
        style={picture ? { display: 'none' } : {}}
      >
        <svg className="w-1/2 h-1/2" fill="currentColor" viewBox="0 0 20 20">
          <path fillRule="evenodd" d="M10 9a3 3 0 100-6 3 3 0 000 6zm-7 9a7 7 0 1114 0H3z" clipRule="evenodd" />
        </svg>
      </div>
    </div>
  );
}
