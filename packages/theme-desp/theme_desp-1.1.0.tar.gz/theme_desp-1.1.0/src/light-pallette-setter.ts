import { BasePalletteSetter } from './pallette-setter';

export class LightPalletteSetter implements BasePalletteSetter {
  name: string = 'Desp Theme Light';
  type: 'dark' | 'light' = 'light';
  setColorPallette() {
    /**
     * Borders
     */
    document.documentElement.style.setProperty(
      '--jp-border-color0',
      'var(--md-grey-400)'
    );
    document.documentElement.style.setProperty(
      '--jp-border-color1',
      'var(--md-grey-400)'
    );
    document.documentElement.style.setProperty(
      '--jp-border-color2',
      'var(--md-grey-300)'
    );
    document.documentElement.style.setProperty(
      '--jp-border-color3',
      'var(--md-grey-200)'
    );

    /**
     * Defaults use Material Design specification
     */
    document.documentElement.style.setProperty(
      '--jp-ui-font-color0',
      'rgba(0, 0, 0, 1)'
    );
    document.documentElement.style.setProperty(
      '--jp-ui-font-color1',
      'rgba(0, 0, 0, 0.87)'
    );
    document.documentElement.style.setProperty(
      '--jp-ui-font-color2',
      'rgba(0, 0, 0, 0.54)'
    );
    document.documentElement.style.setProperty(
      '--jp-ui-font-color3',
      'rgba(0, 0, 0, 0.38)'
    );

    /**
     * Defaults use Material Design specification
     */
    document.documentElement.style.setProperty(
      '--jp-content-font-color0',
      'rgba(0, 0, 0, 1)'
    );
    document.documentElement.style.setProperty(
      '--jp-content-font-color1',
      'rgba(0, 0, 0, 0.87)'
    );
    document.documentElement.style.setProperty(
      '--jp-content-font-color2',
      'rgba(0, 0, 0, 0.54)'
    );
    document.documentElement.style.setProperty(
      '--jp-content-font-color3',
      'rgba(0, 0, 0, 0.38)'
    );

    /**
     * Layout
     */
    document.documentElement.style.setProperty('--jp-layout-color0', 'white');
    document.documentElement.style.setProperty('--jp-layout-color1', 'white');
    document.documentElement.style.setProperty(
      '--jp-layout-color2',
      'var(--md-grey-200)'
    );
    document.documentElement.style.setProperty('--jp-layout-color3', '#7B34DB');
    document.documentElement.style.setProperty(
      '--jp-layout-color4',
      'var(--md-grey-600)'
    );

    /**
     * Inverse Layout
     */
    document.documentElement.style.setProperty(
      '--jp-inverse-layout-color0',
      '#111111'
    );
    document.documentElement.style.setProperty(
      '--jp-inverse-layout-color1',
      'var(--md-grey-900)'
    );
    document.documentElement.style.setProperty(
      '--jp-inverse-layout-color2',
      'var(--md-grey-800)'
    );
    document.documentElement.style.setProperty(
      '--jp-inverse-layout-color3',
      'var(--md-grey-700)'
    );
    document.documentElement.style.setProperty(
      '--jp-inverse-layout-color4',
      'var(--md-grey-600)'
    );

    /**
     * State colors (warn, error, success, info)
     */
    document.documentElement.style.setProperty(
      '--jp-warn-color0',
      'var(--md-purple-700)'
    );
    document.documentElement.style.setProperty(
      '--jp-warn-color1',
      'var(--md-purple-500)'
    );
    document.documentElement.style.setProperty(
      '--jp-warn-color2',
      'var(--md-purple-300)'
    );
    document.documentElement.style.setProperty(
      '--jp-warn-color3',
      'var(--md-purple-100)'
    );

    /**
     * Cell specific styles
     */
    document.documentElement.style.setProperty(
      '--jp-cell-editor-background',
      'var(--md-grey-100)'
    );
    document.documentElement.style.setProperty(
      '--jp-cell-prompt-not-active-font-color',
      'var(--md-grey-700)'
    );

    /**
     * Rendermime styles
     */
    document.documentElement.style.setProperty(
      '--jp-rendermime-error-background',
      '#fdd'
    );

    document.documentElement.style.setProperty(
      '--jp-rendermime-table-row-background',
      'var(--md-grey-100)'
    );

    document.documentElement.style.setProperty(
      '--jp-rendermime-table-row-hover-background',
      'var(--md-grey-200)'
    );

    /**
     * Code mirror specific styles
     */
    document.documentElement.style.setProperty(
      '--jp-mirror-editor-operator-color',
      '#aa22ff'
    );
    document.documentElement.style.setProperty(
      '--jp-mirror-editor-meta-color',
      '#aa22ff'
    );
    document.documentElement.style.setProperty(
      '--jp-mirror-editor-attribute-color',
      '#00c'
    );
  }
}
