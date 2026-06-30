import {
  KundaliInput,
  KundaliResponse,
  ChatResponse,
  MuhurtaResponse,
  HealthResponse,
  EventType,
  MatchInput,
  MatchResponse,
  GemstoneResponse,
  PanchangRequest,
  PanchangResponse,
  RashifalData,
  RashifalPeriod,
  NumerologyResponse,
  NumerologyCompatibilityResponse,
  BusinessNumerologyResponse,
  NameSuggestion,
} from './types';

const API_BASE = process.env.NEXT_PUBLIC_API_BASE || 'http://localhost:8000/api';

class ApiError extends Error {
  constructor(message: string, public statusCode?: number) {
    super(message);
    this.name = 'ApiError';
  }
}

async function handleResponse<T>(response: Response): Promise<T> {
  if (!response.ok) {
    const errorText = await response.text();
    throw new ApiError(
      errorText || `HTTP error! status: ${response.status}`,
      response.status
    );
  }
  return response.json();
}

/**
 * Generate a new Kundali from birth details
 */
export async function generateKundali(data: KundaliInput): Promise<KundaliResponse> {
  try {
    const response = await fetch(`${API_BASE}/generate`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(data),
      credentials: 'include', // Include cookies for session
    });

    return handleResponse<KundaliResponse>(response);
  } catch (error) {
    if (error instanceof ApiError) {
      throw error;
    }
    throw new ApiError(`Failed to generate kundali: ${error instanceof Error ? error.message : 'Unknown error'}`);
  }
}

/**
 * Send a chat message to the AI assistant
 */
export async function sendChatMessage(
  kundaliId: string,
  question: string
): Promise<ChatResponse> {
  try {
    const response = await fetch(`${API_BASE}/chat`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        kundali_id: kundaliId,
        question: question,
      }),
      credentials: 'include',
    });

    return handleResponse<ChatResponse>(response);
  } catch (error) {
    if (error instanceof ApiError) {
      throw error;
    }
    throw new ApiError(`Failed to send chat message: ${error instanceof Error ? error.message : 'Unknown error'}`);
  }
}

/**
 * Find auspicious Muhurta (timing) for an event
 */
export async function findMuhurta(
  kundaliId: string,
  eventType: EventType,
  year: number
): Promise<MuhurtaResponse> {
  try {
    const response = await fetch(`${API_BASE}/muhurta`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        kundali_id: kundaliId,
        event_type: eventType,
        year: year,
      }),
      credentials: 'include',
    });

    return handleResponse<MuhurtaResponse>(response);
  } catch (error) {
    if (error instanceof ApiError) {
      throw error;
    }
    throw new ApiError(`Failed to find muhurta: ${error instanceof Error ? error.message : 'Unknown error'}`);
  }
}

/**
 * Get health predictions for a date range
 */
export async function getHealthPredictions(
  kundaliId: string,
  startYear: number,
  endYear: number
): Promise<HealthResponse> {
  try {
    const response = await fetch(`${API_BASE}/health`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        kundali_id: kundaliId,
        start_year: startYear,
        end_year: endYear,
      }),
      credentials: 'include',
    });

    return handleResponse<HealthResponse>(response);
  } catch (error) {
    if (error instanceof ApiError) {
      throw error;
    }
    throw new ApiError(`Failed to get health predictions: ${error instanceof Error ? error.message : 'Unknown error'}`);
  }
}

/**
 * Match two Kundalis for marriage compatibility
 */
export async function matchKundalis(data: MatchInput): Promise<MatchResponse> {
  try {
    const response = await fetch(`${API_BASE}/match`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(data),
      credentials: 'include',
    });

    return handleResponse<MatchResponse>(response);
  } catch (error) {
    if (error instanceof ApiError) {
      throw error;
    }
    throw new ApiError(`Failed to match kundalis: ${error instanceof Error ? error.message : 'Unknown error'}`);
  }
}

/**
 * Get gemstone recommendations for a Kundali
 */
export async function getGemstoneRecommendations(
  kundaliId: string
): Promise<GemstoneResponse> {
  try {
    const response = await fetch(`${API_BASE}/gemstone/analyze`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        kundali_id: kundaliId,
      }),
      credentials: 'include',
    });

    return handleResponse<GemstoneResponse>(response);
  } catch (error) {
    if (error instanceof ApiError) {
      throw error;
    }
    throw new ApiError(`Failed to get gemstone recommendations: ${error instanceof Error ? error.message : 'Unknown error'}`);
  }
}

/**
 * Get daily Panchang data
 */
export async function getDailyPanchang(data: PanchangRequest): Promise<PanchangResponse> {
  try {
    const response = await fetch(`${API_BASE}/panchang/daily`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(data),
      credentials: 'include',
    });

    return handleResponse<PanchangResponse>(response);
  } catch (error) {
    if (error instanceof ApiError) {
      throw error;
    }
    throw new ApiError(`Failed to get Panchang: ${error instanceof Error ? error.message : 'Unknown error'}`);
  }
}

/**
 * Get today's Panchang
 */
export async function getTodayPanchang(
  latitude: number = 28.6139,
  longitude: number = 77.2090,
  timezone: string = "Asia/Kolkata",
  location: string = "Delhi"
): Promise<PanchangResponse> {
  try {
    const params = new URLSearchParams({
      latitude: latitude.toString(),
      longitude: longitude.toString(),
      timezone,
      location,
    });

    const response = await fetch(`${API_BASE}/panchang/today?${params}`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      },
      credentials: 'include',
    });

    return handleResponse<PanchangResponse>(response);
  } catch (error) {
    if (error instanceof ApiError) {
      throw error;
    }
    throw new ApiError(`Failed to get today's Panchang: ${error instanceof Error ? error.message : 'Unknown error'}`);
  }
}

/**
 * Get Rashifal (horoscope) for a specific rashi
 */
export async function getRashifal(
  rashiNum: number,
  period: RashifalPeriod = 'daily'
): Promise<RashifalData> {
  try {
    const params = new URLSearchParams({
      rashi: rashiNum.toString(),
      period,
    });

    const response = await fetch(`${API_BASE}/rashifal?${params}`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      },
      credentials: 'include',
    });

    return handleResponse<RashifalData>(response);
  } catch (error) {
    if (error instanceof ApiError) {
      throw error;
    }
    throw new ApiError(`Failed to get rashifal: ${error instanceof Error ? error.message : 'Unknown error'}`);
  }
}

/**
 * Get Rashifal for all 12 rashis
 */
export async function getAllRashifal(
  period: RashifalPeriod = 'daily'
): Promise<RashifalData[]> {
  try {
    const params = new URLSearchParams({
      period,
    });

    const response = await fetch(`${API_BASE}/rashifal/all?${params}`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      },
      credentials: 'include',
    });

    return handleResponse<RashifalData[]>(response);
  } catch (error) {
    if (error instanceof ApiError) {
      throw error;
    }
    throw new ApiError(`Failed to get all rashifal: ${error instanceof Error ? error.message : 'Unknown error'}`);
  }
}

/**
 * Download Kundali PDF report
 * Uses stored kundali parameters to regenerate PDF (works even after server restart)
 */
export async function downloadKundaliPDF(kundaliId: string): Promise<void> {
  try {
    // Get stored kundali parameters from sessionStorage
    const currentKundali = sessionStorage.getItem('current_kundali');

    let response: Response;

    if (currentKundali) {
      // Use POST endpoint with parameters (more reliable)
      const params = JSON.parse(currentKundali);
      response = await fetch(`${API_BASE}/kundali/pdf`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          name: params.name,
          dob: params.dob,
          tob: params.tob,
          city: params.city,
          latitude: params.latitude,
          longitude: params.longitude,
          timezone: 'Asia/Kolkata'
        }),
        credentials: 'include',
      });
    } else {
      // Fallback to GET endpoint with kundali_id
      response = await fetch(`${API_BASE}/kundali/${kundaliId}/pdf`, {
        method: 'GET',
        credentials: 'include',
      });
    }

    if (!response.ok) {
      const errorText = await response.text();
      throw new ApiError(
        errorText || `HTTP error! status: ${response.status}`,
        response.status
      );
    }

    // Get the blob from response
    const blob = await response.blob();

    // Extract filename from Content-Disposition header if available
    const contentDisposition = response.headers.get('Content-Disposition');
    let filename = 'Kundali_Report.pdf';
    if (contentDisposition) {
      const match = contentDisposition.match(/filename=(.+)/);
      if (match && match[1]) {
        filename = match[1].replace(/"/g, '');
      }
    }

    // Create download link and trigger download
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    window.URL.revokeObjectURL(url);
    document.body.removeChild(a);

  } catch (error) {
    if (error instanceof ApiError) {
      throw error;
    }
    throw new ApiError(`Failed to download PDF: ${error instanceof Error ? error.message : 'Unknown error'}`);
  }
}

/**
 * Download Matching PDF report
 */
export async function downloadMatchingPDF(data: MatchInput): Promise<void> {
  try {
    const response = await fetch(`${API_BASE}/matching/pdf`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(data),
      credentials: 'include',
    });

    if (!response.ok) {
      const errorText = await response.text();
      throw new ApiError(
        errorText || `HTTP error! status: ${response.status}`,
        response.status
      );
    }

    // Get the blob from response
    const blob = await response.blob();

    // Extract filename from Content-Disposition header if available
    const contentDisposition = response.headers.get('Content-Disposition');
    let filename = 'Matching_Report.pdf';
    if (contentDisposition) {
      const match = contentDisposition.match(/filename=(.+)/);
      if (match && match[1]) {
        filename = match[1].replace(/"/g, '');
      }
    }

    // Create download link and trigger download
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    window.URL.revokeObjectURL(url);
    document.body.removeChild(a);

  } catch (error) {
    if (error instanceof ApiError) {
      throw error;
    }
    throw new ApiError(`Failed to download PDF: ${error instanceof Error ? error.message : 'Unknown error'}`);
  }
}

// =============================================================================
// NUMEROLOGY API FUNCTIONS
// =============================================================================

/**
 * Analyze numerology for a person
 */
export async function analyzeNumerology(
  name: string,
  birthDate: string
): Promise<NumerologyResponse> {
  try {
    const response = await fetch(`${API_BASE}/numerology/analyze`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        name: name,
        birth_date: birthDate,
      }),
      credentials: 'include',
    });

    return handleResponse<NumerologyResponse>(response);
  } catch (error) {
    if (error instanceof ApiError) {
      throw error;
    }
    throw new ApiError(`Failed to analyze numerology: ${error instanceof Error ? error.message : 'Unknown error'}`);
  }
}

/**
 * Check numerology compatibility between two people
 */
export async function checkNumerologyCompatibility(
  person1Name: string,
  person1Dob: string,
  person2Name: string,
  person2Dob: string
): Promise<NumerologyCompatibilityResponse> {
  try {
    const response = await fetch(`${API_BASE}/numerology/compatibility`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        person1_name: person1Name,
        person1_dob: person1Dob,
        person2_name: person2Name,
        person2_dob: person2Dob,
      }),
      credentials: 'include',
    });

    return handleResponse<NumerologyCompatibilityResponse>(response);
  } catch (error) {
    if (error instanceof ApiError) {
      throw error;
    }
    throw new ApiError(`Failed to check compatibility: ${error instanceof Error ? error.message : 'Unknown error'}`);
  }
}

/**
 * Analyze business name numerology
 */
export async function analyzeBusinessName(
  businessName: string,
  ownerDob: string
): Promise<BusinessNumerologyResponse> {
  try {
    const response = await fetch(`${API_BASE}/numerology/business`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        business_name: businessName,
        owner_dob: ownerDob,
      }),
      credentials: 'include',
    });

    return handleResponse<BusinessNumerologyResponse>(response);
  } catch (error) {
    if (error instanceof ApiError) {
      throw error;
    }
    throw new ApiError(`Failed to analyze business name: ${error instanceof Error ? error.message : 'Unknown error'}`);
  }
}

/**
 * Get name correction suggestions
 */
export async function suggestNameCorrections(
  name: string,
  birthDate: string,
  targetNumber?: number
): Promise<NameSuggestion[]> {
  try {
    const response = await fetch(`${API_BASE}/numerology/suggest-name`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        name: name,
        birth_date: birthDate,
        target_number: targetNumber,
      }),
      credentials: 'include',
    });

    return handleResponse<NameSuggestion[]>(response);
  } catch (error) {
    if (error instanceof ApiError) {
      throw error;
    }
    throw new ApiError(`Failed to get name suggestions: ${error instanceof Error ? error.message : 'Unknown error'}`);
  }
}

// =============================================================================
// KUNDALI ANALYSIS HELPER
// =============================================================================

export interface KundaliAnalysisData {
  planets: Record<string, any>;
  lagna: Record<string, any>;
  houses: Record<string, string[]>;
  birth_data: Record<string, any>;
}

export interface SavedKundaliParams {
  name: string;
  dob: string;
  tob: string;
  city: string;
  latitude: number | null;
  longitude: number | null;
}

/**
 * Regenerate a kundali from saved birth parameters and get analysis data.
 * This is the recommended way to get kundali data for analysis pages.
 *
 * @param params Saved birth parameters (name, dob, tob, city, lat/long)
 * @returns Kundali analysis data suitable for dosha, career, remedies APIs
 */
export async function getKundaliDataForAnalysis(
  params: SavedKundaliParams
): Promise<KundaliAnalysisData> {
  // Step 1: Regenerate kundali from birth parameters
  const generateResponse = await fetch(`${API_BASE}/generate`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      name: params.name,
      dob: params.dob,
      tob: params.tob,
      city: params.city,
      latitude: params.latitude,
      longitude: params.longitude,
    }),
    credentials: 'include',
  });

  if (!generateResponse.ok) {
    throw new ApiError('कुंडली जनरेट नहीं हो सकी। कृपया दोबारा कोशिश करें।', generateResponse.status);
  }

  const generateResult = await generateResponse.json();

  // Step 2: Fetch analysis data
  const dataResponse = await fetch(`${API_BASE}/kundali/${generateResult.kundali_id}/data`, {
    credentials: 'include',
  });

  if (!dataResponse.ok) {
    throw new ApiError('कुंडली डेटा लोड नहीं हो सका।', dataResponse.status);
  }

  const dataResult = await dataResponse.json();
  return dataResult.kundali_data;
}

export { ApiError };
