'use client';

import React, { useState, useEffect } from 'react';
import { Modal } from './ui/Modal';
import { Button } from './ui/Button';
import {
  SavedKundali,
  DEFAULT_CATEGORIES,
  saveKundali,
  updateKundali,
  getAllTags,
} from '@/lib/storage';

interface SaveKundaliModalProps {
  isOpen: boolean;
  onClose: () => void;
  kundaliData: {
    name: string;
    dob: string;
    tob: string;
    city: string;
    latitude: number | null;
    longitude: number | null;
    kundali_id: string;
  };
  editingKundali?: SavedKundali | null;
  onSaved?: (kundali: SavedKundali) => void;
}

export function SaveKundaliModal({
  isOpen,
  onClose,
  kundaliData,
  editingKundali,
  onSaved,
}: SaveKundaliModalProps) {
  const [name, setName] = useState('');
  const [category, setCategory] = useState('');
  const [tags, setTags] = useState<string[]>([]);
  const [tagInput, setTagInput] = useState('');
  const [notes, setNotes] = useState('');
  const [existingTags, setExistingTags] = useState<string[]>([]);
  const [isSaving, setIsSaving] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState(false);

  const isEditing = !!editingKundali;

  // Load existing tags on mount
  useEffect(() => {
    setExistingTags(getAllTags());
  }, [isOpen]);

  // Reset form when modal opens
  useEffect(() => {
    if (isOpen) {
      if (editingKundali) {
        setName(editingKundali.name);
        setCategory(editingKundali.category || '');
        setTags(editingKundali.tags || []);
        setNotes(editingKundali.notes || '');
      } else {
        setName(kundaliData.name || '');
        setCategory('');
        setTags([]);
        setNotes('');
      }
      setError(null);
      setSuccess(false);
    }
  }, [isOpen, editingKundali, kundaliData.name]);

  const handleAddTag = () => {
    const trimmedTag = tagInput.trim().toLowerCase();
    if (trimmedTag && !tags.includes(trimmedTag)) {
      setTags([...tags, trimmedTag]);
      setTagInput('');
    }
  };

  const handleRemoveTag = (tagToRemove: string) => {
    setTags(tags.filter(t => t !== tagToRemove));
  };

  const handleTagKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter') {
      e.preventDefault();
      handleAddTag();
    }
  };

  const handleSave = async () => {
    if (!name.trim()) {
      setError('Please enter a name');
      return;
    }

    setIsSaving(true);
    setError(null);

    try {
      let savedKundali: SavedKundali | null = null;

      if (isEditing && editingKundali) {
        // Update existing
        savedKundali = updateKundali(editingKundali.id, {
          name: name.trim(),
          category: category || undefined,
          tags: tags.length > 0 ? tags : undefined,
          notes: notes.trim() || undefined,
        });

        if (!savedKundali) {
          throw new Error('Failed to update Kundali');
        }
      } else {
        // Save new
        savedKundali = saveKundali({
          name: name.trim(),
          dob: kundaliData.dob,
          tob: kundaliData.tob,
          city: kundaliData.city,
          latitude: kundaliData.latitude,
          longitude: kundaliData.longitude,
          kundali_id: kundaliData.kundali_id,
          category: category || undefined,
          tags: tags.length > 0 ? tags : undefined,
          notes: notes.trim() || undefined,
        });
      }

      setSuccess(true);

      if (onSaved && savedKundali) {
        onSaved(savedKundali);
      }

      // Close after short delay to show success
      setTimeout(() => {
        onClose();
      }, 1000);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to save');
    } finally {
      setIsSaving(false);
    }
  };

  return (
    <Modal
      isOpen={isOpen}
      onClose={onClose}
      title={isEditing ? 'कुंडली संपादित करें / Edit Kundali' : 'कुंडली सेव करें / Save Kundali'}
      titleIcon={isEditing ? '✏️' : '💾'}
    >
      <div className="space-y-5">
        {/* Success Message */}
        {success && (
          <div className="p-4 bg-green-50 border border-green-200 rounded-lg flex items-center gap-3">
            <div className="text-green-500 text-2xl">✓</div>
            <div>
              <p className="font-medium text-green-800">
                {isEditing ? 'कुंडली अपडेट हो गई!' : 'कुंडली सेव हो गई!'}
              </p>
              <p className="text-sm text-green-600">
                {isEditing ? 'Kundali updated successfully!' : 'Kundali saved successfully!'}
              </p>
            </div>
          </div>
        )}

        {/* Error Message */}
        {error && (
          <div className="p-3 bg-red-50 border-l-4 border-red-500 rounded-r-lg text-red-700 flex items-center gap-2">
            <span>Error</span>
            <span>{error}</span>
          </div>
        )}

        {/* Kundali Info Preview */}
        <div className="bg-orange-50 rounded-lg p-4 border border-orange-200">
          <h3 className="font-medium text-orange-800 mb-2 flex items-center gap-2">
            <span>Birth Details / जन्म विवरण</span>
          </h3>
          <div className="grid grid-cols-2 gap-3 text-sm">
            <div>
              <span className="text-gray-500">तिथि / Date:</span>
              <span className="ml-2 font-medium">{kundaliData.dob}</span>
            </div>
            <div>
              <span className="text-gray-500">समय / Time:</span>
              <span className="ml-2 font-medium">{kundaliData.tob}</span>
            </div>
            <div className="col-span-2">
              <span className="text-gray-500">स्थान / Place:</span>
              <span className="ml-2 font-medium">{kundaliData.city}</span>
            </div>
          </div>
        </div>

        {/* Name Input */}
        <div>
          <label className="block mb-1.5 font-medium text-gray-700 text-sm">
            <span className="text-orange-500">नाम</span>
            <span className="text-gray-400 text-xs ml-1">/ Name *</span>
          </label>
          <input
            type="text"
            value={name}
            onChange={(e) => setName(e.target.value)}
            placeholder="नाम लिखें... / Enter name..."
            className="w-full px-3 py-2.5 border border-gray-200 rounded-lg focus:border-orange-500 focus:ring-1 focus:ring-orange-200 transition-all text-sm"
            disabled={success}
          />
        </div>

        {/* Category Select */}
        <div>
          <label className="block mb-1.5 font-medium text-gray-700 text-sm">
            <span className="text-orange-500">श्रेणी</span>
            <span className="text-gray-400 text-xs ml-1">/ Category</span>
          </label>
          <select
            value={category}
            onChange={(e) => setCategory(e.target.value)}
            className="w-full px-3 py-2.5 border border-gray-200 rounded-lg focus:border-orange-500 focus:ring-1 focus:ring-orange-200 transition-all text-sm bg-white"
            disabled={success}
          >
            <option value="">श्रेणी चुनें / Select category...</option>
            {DEFAULT_CATEGORIES.map((cat) => (
              <option key={cat.id} value={cat.id}>
                {cat.icon} {cat.nameHindi} / {cat.name}
              </option>
            ))}
          </select>
        </div>

        {/* Tags */}
        <div>
          <label className="block mb-1.5 font-medium text-gray-700 text-sm">
            <span className="text-orange-500">टैग</span>
            <span className="text-gray-400 text-xs ml-1">/ Tags</span>
          </label>
          <div className="flex gap-2">
            <input
              type="text"
              value={tagInput}
              onChange={(e) => setTagInput(e.target.value)}
              onKeyPress={handleTagKeyPress}
              placeholder="टैग जोड़ें / Add tag..."
              className="flex-1 px-3 py-2 border border-gray-200 rounded-lg focus:border-orange-500 focus:ring-1 focus:ring-orange-200 transition-all text-sm"
              disabled={success}
              list="existing-tags"
            />
            <datalist id="existing-tags">
              {existingTags.map(t => (
                <option key={t} value={t} />
              ))}
            </datalist>
            <button
              type="button"
              onClick={handleAddTag}
              disabled={success || !tagInput.trim()}
              className="px-4 py-2 bg-orange-100 text-orange-700 rounded-lg hover:bg-orange-200 transition-colors disabled:opacity-50"
            >
              +
            </button>
          </div>

          {/* Tags Display */}
          {tags.length > 0 && (
            <div className="flex flex-wrap gap-2 mt-2">
              {tags.map((tag) => (
                <span
                  key={tag}
                  className="inline-flex items-center gap-1 px-2 py-1 bg-orange-100 text-orange-700 rounded-full text-xs"
                >
                  #{tag}
                  <button
                    type="button"
                    onClick={() => handleRemoveTag(tag)}
                    className="hover:text-orange-900"
                    disabled={success}
                  >
                    x
                  </button>
                </span>
              ))}
            </div>
          )}
        </div>

        {/* Notes */}
        <div>
          <label className="block mb-1.5 font-medium text-gray-700 text-sm">
            <span className="text-orange-500">नोट्स</span>
            <span className="text-gray-400 text-xs ml-1">/ Notes (optional)</span>
          </label>
          <textarea
            value={notes}
            onChange={(e) => setNotes(e.target.value)}
            placeholder="नोट्स जोड़ें / Add any notes..."
            rows={3}
            className="w-full px-3 py-2.5 border border-gray-200 rounded-lg focus:border-orange-500 focus:ring-1 focus:ring-orange-200 transition-all text-sm resize-none"
            disabled={success}
          />
        </div>

        {/* Actions */}
        <div className="flex justify-end gap-3 pt-4 border-t">
          <Button
            variant="outline"
            onClick={onClose}
            disabled={isSaving}
          >
            {success ? 'बंद करें / Close' : 'रद्द करें / Cancel'}
          </Button>
          {!success && (
            <Button
              variant="primary"
              onClick={handleSave}
              isLoading={isSaving}
            >
              {isEditing ? 'अपडेट / Update' : 'सेव / Save'}
            </Button>
          )}
        </div>
      </div>
    </Modal>
  );
}
