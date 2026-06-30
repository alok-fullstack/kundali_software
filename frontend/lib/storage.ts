/**
 * Kundali Storage Types and Utilities
 * Local storage management for saved Kundalis
 */

// =============================================================================
// TYPES
// =============================================================================

export interface SavedKundali {
  id: string;
  name: string;
  dob: string;           // YYYY-MM-DD
  tob: string;           // HH:MM
  city: string;
  latitude: number | null;
  longitude: number | null;
  kundali_id: string;    // Backend generated ID
  savedAt: string;       // ISO date string
  updatedAt?: string;    // ISO date string
  category?: string;     // Family grouping
  tags?: string[];       // Custom tags
  notes?: string;        // User notes
  // Cached astrological data for quick comparison
  moonRashi?: string;
  moonNakshatra?: string;
  lagnaRashi?: string;
}

export interface KundaliCategory {
  id: string;
  name: string;
  nameHindi: string;
  color: string;
  icon: string;
}

export interface ComparisonResult {
  kundali1: SavedKundali;
  kundali2: SavedKundali;
  comparedAt: string;
}

// =============================================================================
// DEFAULT CATEGORIES
// =============================================================================

export const DEFAULT_CATEGORIES: KundaliCategory[] = [
  { id: 'family', name: 'Family', nameHindi: 'परिवार', color: '#ff6b35', icon: '👨‍👩‍👧‍👦' },
  { id: 'relatives', name: 'Relatives', nameHindi: 'रिश्तेदार', color: '#9c27b0', icon: '👥' },
  { id: 'friends', name: 'Friends', nameHindi: 'मित्र', color: '#2196f3', icon: '🤝' },
  { id: 'prospective', name: 'Prospective Match', nameHindi: 'विवाह संबंध', color: '#e91e63', icon: '💑' },
  { id: 'children', name: 'Children', nameHindi: 'बच्चे', color: '#4caf50', icon: '👶' },
  { id: 'other', name: 'Other', nameHindi: 'अन्य', color: '#607d8b', icon: '📋' },
];

// =============================================================================
// STORAGE KEYS
// =============================================================================

const STORAGE_KEYS = {
  SAVED_KUNDALIS: 'kundali_saved_list',
  CATEGORIES: 'kundali_categories',
  RECENT_COMPARISONS: 'kundali_recent_comparisons',
  SETTINGS: 'kundali_storage_settings',
};

// =============================================================================
// UTILITY FUNCTIONS
// =============================================================================

/**
 * Generate a unique ID
 */
export function generateId(): string {
  return `k_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
}

/**
 * Check if localStorage is available
 */
export function isStorageAvailable(): boolean {
  if (typeof window === 'undefined') return false;
  try {
    const test = '__storage_test__';
    localStorage.setItem(test, test);
    localStorage.removeItem(test);
    return true;
  } catch {
    return false;
  }
}

// =============================================================================
// KUNDALI STORAGE FUNCTIONS
// =============================================================================

/**
 * Get all saved Kundalis
 */
export function getSavedKundalis(): SavedKundali[] {
  if (!isStorageAvailable()) return [];
  try {
    const data = localStorage.getItem(STORAGE_KEYS.SAVED_KUNDALIS);
    if (!data) return [];
    const kundalis = JSON.parse(data);
    // Sort by savedAt descending (newest first)
    return kundalis.sort((a: SavedKundali, b: SavedKundali) =>
      new Date(b.savedAt).getTime() - new Date(a.savedAt).getTime()
    );
  } catch (error) {
    console.error('Failed to get saved kundalis:', error);
    return [];
  }
}

/**
 * Get a single saved Kundali by ID
 */
export function getSavedKundaliById(id: string): SavedKundali | null {
  const kundalis = getSavedKundalis();
  return kundalis.find(k => k.id === id) || null;
}

/**
 * Get Kundalis by category
 */
export function getKundalisByCategory(category: string): SavedKundali[] {
  const kundalis = getSavedKundalis();
  return kundalis.filter(k => k.category === category);
}

/**
 * Get Kundalis by tag
 */
export function getKundalisByTag(tag: string): SavedKundali[] {
  const kundalis = getSavedKundalis();
  return kundalis.filter(k => k.tags?.includes(tag));
}

/**
 * Search Kundalis by name or city
 */
export function searchKundalis(query: string): SavedKundali[] {
  const kundalis = getSavedKundalis();
  const lowerQuery = query.toLowerCase();
  return kundalis.filter(k =>
    k.name.toLowerCase().includes(lowerQuery) ||
    k.city.toLowerCase().includes(lowerQuery) ||
    k.tags?.some(t => t.toLowerCase().includes(lowerQuery))
  );
}

/**
 * Save a new Kundali
 */
export function saveKundali(kundali: Omit<SavedKundali, 'id' | 'savedAt'>): SavedKundali {
  if (!isStorageAvailable()) {
    throw new Error('Storage not available');
  }

  const kundalis = getSavedKundalis();
  const newKundali: SavedKundali = {
    ...kundali,
    id: generateId(),
    savedAt: new Date().toISOString(),
  };

  kundalis.unshift(newKundali); // Add to beginning

  try {
    localStorage.setItem(STORAGE_KEYS.SAVED_KUNDALIS, JSON.stringify(kundalis));
    return newKundali;
  } catch (error) {
    console.error('Failed to save kundali:', error);
    throw new Error('Failed to save Kundali. Storage may be full.');
  }
}

/**
 * Update an existing Kundali
 */
export function updateKundali(id: string, updates: Partial<SavedKundali>): SavedKundali | null {
  if (!isStorageAvailable()) return null;

  const kundalis = getSavedKundalis();
  const index = kundalis.findIndex(k => k.id === id);

  if (index === -1) return null;

  const updated: SavedKundali = {
    ...kundalis[index],
    ...updates,
    id: kundalis[index].id, // Preserve original ID
    savedAt: kundalis[index].savedAt, // Preserve original save date
    updatedAt: new Date().toISOString(),
  };

  kundalis[index] = updated;

  try {
    localStorage.setItem(STORAGE_KEYS.SAVED_KUNDALIS, JSON.stringify(kundalis));
    return updated;
  } catch (error) {
    console.error('Failed to update kundali:', error);
    return null;
  }
}

/**
 * Delete a Kundali
 */
export function deleteKundali(id: string): boolean {
  if (!isStorageAvailable()) return false;

  const kundalis = getSavedKundalis();
  const filtered = kundalis.filter(k => k.id !== id);

  if (filtered.length === kundalis.length) return false;

  try {
    localStorage.setItem(STORAGE_KEYS.SAVED_KUNDALIS, JSON.stringify(filtered));
    return true;
  } catch (error) {
    console.error('Failed to delete kundali:', error);
    return false;
  }
}

/**
 * Delete multiple Kundalis
 */
export function deleteMultipleKundalis(ids: string[]): number {
  if (!isStorageAvailable()) return 0;

  const kundalis = getSavedKundalis();
  const filtered = kundalis.filter(k => !ids.includes(k.id));
  const deletedCount = kundalis.length - filtered.length;

  try {
    localStorage.setItem(STORAGE_KEYS.SAVED_KUNDALIS, JSON.stringify(filtered));
    return deletedCount;
  } catch (error) {
    console.error('Failed to delete kundalis:', error);
    return 0;
  }
}

// =============================================================================
// CATEGORY FUNCTIONS
// =============================================================================

/**
 * Get all categories (custom + default)
 */
export function getCategories(): KundaliCategory[] {
  if (!isStorageAvailable()) return DEFAULT_CATEGORIES;

  try {
    const data = localStorage.getItem(STORAGE_KEYS.CATEGORIES);
    if (!data) return DEFAULT_CATEGORIES;
    return JSON.parse(data);
  } catch {
    return DEFAULT_CATEGORIES;
  }
}

/**
 * Add a custom category
 */
export function addCategory(category: Omit<KundaliCategory, 'id'>): KundaliCategory {
  const categories = getCategories();
  const newCategory: KundaliCategory = {
    ...category,
    id: `cat_${Date.now()}`,
  };

  categories.push(newCategory);
  localStorage.setItem(STORAGE_KEYS.CATEGORIES, JSON.stringify(categories));
  return newCategory;
}

// =============================================================================
// EXPORT/IMPORT FUNCTIONS
// =============================================================================

/**
 * Export all saved Kundalis to JSON
 */
export function exportKundalis(): string {
  const kundalis = getSavedKundalis();
  const categories = getCategories();

  const exportData = {
    version: '1.0',
    exportedAt: new Date().toISOString(),
    kundalis,
    categories,
  };

  return JSON.stringify(exportData, null, 2);
}

/**
 * Export selected Kundalis to JSON
 */
export function exportSelectedKundalis(ids: string[]): string {
  const kundalis = getSavedKundalis().filter(k => ids.includes(k.id));

  const exportData = {
    version: '1.0',
    exportedAt: new Date().toISOString(),
    kundalis,
    partial: true,
  };

  return JSON.stringify(exportData, null, 2);
}

/**
 * Import Kundalis from JSON
 */
export function importKundalis(jsonString: string, overwrite: boolean = false): { imported: number; skipped: number; errors: string[] } {
  const result = { imported: 0, skipped: 0, errors: [] as string[] };

  if (!isStorageAvailable()) {
    result.errors.push('Storage not available');
    return result;
  }

  try {
    const data = JSON.parse(jsonString);

    if (!data.kundalis || !Array.isArray(data.kundalis)) {
      result.errors.push('Invalid file format: kundalis array not found');
      return result;
    }

    const existingKundalis = overwrite ? [] : getSavedKundalis();
    const existingIds = new Set(existingKundalis.map(k => k.kundali_id));
    const newKundalis: SavedKundali[] = [...existingKundalis];

    for (const kundali of data.kundalis) {
      // Validate required fields
      if (!kundali.name || !kundali.dob || !kundali.tob || !kundali.city || !kundali.kundali_id) {
        result.errors.push(`Skipped invalid kundali: ${kundali.name || 'unnamed'}`);
        result.skipped++;
        continue;
      }

      // Check for duplicates based on kundali_id
      if (existingIds.has(kundali.kundali_id)) {
        result.skipped++;
        continue;
      }

      // Create new entry with fresh ID
      const newKundali: SavedKundali = {
        ...kundali,
        id: generateId(),
        savedAt: kundali.savedAt || new Date().toISOString(),
      };

      newKundalis.push(newKundali);
      existingIds.add(kundali.kundali_id);
      result.imported++;
    }

    localStorage.setItem(STORAGE_KEYS.SAVED_KUNDALIS, JSON.stringify(newKundalis));

    // Import categories if available
    if (data.categories && Array.isArray(data.categories)) {
      const existingCategories = getCategories();
      const categoryIds = new Set(existingCategories.map(c => c.id));

      for (const cat of data.categories) {
        if (!categoryIds.has(cat.id) && !DEFAULT_CATEGORIES.find(dc => dc.id === cat.id)) {
          existingCategories.push(cat);
        }
      }

      localStorage.setItem(STORAGE_KEYS.CATEGORIES, JSON.stringify(existingCategories));
    }

    return result;
  } catch (error) {
    result.errors.push(`Parse error: ${error instanceof Error ? error.message : 'Unknown error'}`);
    return result;
  }
}

// =============================================================================
// COMPARISON HISTORY
// =============================================================================

/**
 * Save a comparison to history
 */
export function saveComparison(kundali1Id: string, kundali2Id: string): void {
  if (!isStorageAvailable()) return;

  try {
    const history = getComparisonHistory();
    const newComparison = {
      kundali1Id,
      kundali2Id,
      comparedAt: new Date().toISOString(),
    };

    // Remove duplicate comparisons
    const filtered = history.filter(
      c => !(c.kundali1Id === kundali1Id && c.kundali2Id === kundali2Id) &&
           !(c.kundali1Id === kundali2Id && c.kundali2Id === kundali1Id)
    );

    filtered.unshift(newComparison);

    // Keep only last 10 comparisons
    const trimmed = filtered.slice(0, 10);

    localStorage.setItem(STORAGE_KEYS.RECENT_COMPARISONS, JSON.stringify(trimmed));
  } catch (error) {
    console.error('Failed to save comparison:', error);
  }
}

/**
 * Get comparison history
 */
export function getComparisonHistory(): Array<{ kundali1Id: string; kundali2Id: string; comparedAt: string }> {
  if (!isStorageAvailable()) return [];

  try {
    const data = localStorage.getItem(STORAGE_KEYS.RECENT_COMPARISONS);
    if (!data) return [];
    return JSON.parse(data);
  } catch {
    return [];
  }
}

// =============================================================================
// STATISTICS
// =============================================================================

/**
 * Get storage statistics
 */
export function getStorageStats(): {
  totalKundalis: number;
  categoryBreakdown: Record<string, number>;
  oldestEntry: string | null;
  newestEntry: string | null;
  storageUsed: number;
} {
  const kundalis = getSavedKundalis();

  const categoryBreakdown: Record<string, number> = {};
  for (const k of kundalis) {
    const cat = k.category || 'uncategorized';
    categoryBreakdown[cat] = (categoryBreakdown[cat] || 0) + 1;
  }

  // Estimate storage used
  let storageUsed = 0;
  try {
    const data = localStorage.getItem(STORAGE_KEYS.SAVED_KUNDALIS);
    storageUsed = data ? new Blob([data]).size : 0;
  } catch {
    // Ignore
  }

  return {
    totalKundalis: kundalis.length,
    categoryBreakdown,
    oldestEntry: kundalis.length > 0 ? kundalis[kundalis.length - 1].savedAt : null,
    newestEntry: kundalis.length > 0 ? kundalis[0].savedAt : null,
    storageUsed,
  };
}

/**
 * Get all unique tags
 */
export function getAllTags(): string[] {
  const kundalis = getSavedKundalis();
  const tagSet = new Set<string>();

  for (const k of kundalis) {
    if (k.tags) {
      k.tags.forEach(t => tagSet.add(t));
    }
  }

  return Array.from(tagSet).sort();
}

/**
 * Clear all saved data
 */
export function clearAllData(): void {
  if (!isStorageAvailable()) return;

  localStorage.removeItem(STORAGE_KEYS.SAVED_KUNDALIS);
  localStorage.removeItem(STORAGE_KEYS.CATEGORIES);
  localStorage.removeItem(STORAGE_KEYS.RECENT_COMPARISONS);
  localStorage.removeItem(STORAGE_KEYS.SETTINGS);
}
