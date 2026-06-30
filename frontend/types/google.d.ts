declare namespace google {
  namespace maps {
    namespace places {
      class Autocomplete {
        constructor(input: HTMLInputElement, opts?: AutocompleteOptions);
        addListener(eventName: string, handler: () => void): void;
        getPlace(): PlaceResult;
      }

      interface AutocompleteOptions {
        types?: string[];
        fields?: string[];
        componentRestrictions?: { country: string | string[] };
      }

      interface PlaceResult {
        formatted_address?: string;
        geometry?: PlaceGeometry;
        name?: string;
        place_id?: string;
      }

      interface PlaceGeometry {
        location?: LatLng;
        viewport?: LatLngBounds;
      }
    }

    class LatLng {
      constructor(lat: number, lng: number);
      lat(): number;
      lng(): number;
    }

    class LatLngBounds {
      constructor(sw?: LatLng, ne?: LatLng);
    }
  }
}

interface Window {
  google: typeof google;
}
