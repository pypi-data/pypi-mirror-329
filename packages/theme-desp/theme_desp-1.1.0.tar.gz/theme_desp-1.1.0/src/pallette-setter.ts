export interface BasePalletteSetter {
  name: string;
  type: 'light' | 'dark';
  setColorPallette: () => void;
}
