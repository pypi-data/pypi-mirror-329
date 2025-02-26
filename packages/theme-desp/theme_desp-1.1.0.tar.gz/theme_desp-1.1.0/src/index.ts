import {
  JupyterFrontEnd,
  JupyterFrontEndPlugin
} from '@jupyterlab/application';
import { IThemeManager } from '@jupyterlab/apputils';

import { DarkPalletteSetter } from './dark-pallette-setter';
import { LightPalletteSetter } from './light-pallette-setter';

import { initAppFooter, initiAppFaviconAndTitle, InitAppHeader } from './utils';
import { appConfig } from './configuration';

import faviconPng from '../style/favicon.png';

initiAppFaviconAndTitle(appConfig.appName, faviconPng);

const plugin: JupyterFrontEndPlugin<void> = {
  id: 'theme-desp:plugin',
  description: 'A JupyterLab extension.',
  autoStart: true,
  requires: [IThemeManager],
  activate: (app: JupyterFrontEnd, manager: IThemeManager) => {
    app.started.then(() => {
      if (appConfig.header.isVisible) {
        InitAppHeader();
      }
      if (appConfig.footer.isVisible) {
        initAppFooter();
      }
    });

    /**
     * Due to the current limitation of not being able to register multiple themes
     * [https://github.com/jupyterlab/jupyterlab/issues/14202]
     * in the same extension when each theme has its own separate CSS file, we
     * handle theme variants by storing the color palette in TypeScript files and
     * loading them dynamically through a script. This approach allows us to load
     * a base theme ('theme-desp/index.css') and then override the necessary color properties
     * based on the selected palette.
     */
    const pallettesSetters = [LightPalletteSetter, DarkPalletteSetter];
    const baseTheme = 'theme-desp/index.css';

    pallettesSetters.forEach(Pallette => {
      const pallette = new Pallette();
      manager.register({
        name: pallette.name,
        isLight: pallette.type === 'light',
        load: () => {
          pallette.setColorPallette();
          return manager.loadCSS(baseTheme);
        },
        unload: () => Promise.resolve(undefined)
      });
    });
  }
};

export default plugin;
