import { LabIcon } from '@jupyterlab/ui-components';

import despBanner from '../style/desp-banner.png';
import despLogo from '../style/desp-logo.png';
import destinationEarthLogo from '../style/destination-earth.png';
import ecmwfLogo from '../style/ecmwf.png';
import esaLogo from '../style/esa.png';
import eumetsatLogo from '../style/eumetsat.png';
import fundedByEULogo from '../style/funded-by-EU.png';
import implementedByLogo from '../style/implemented-by.png';
import appleTouchIcon from '../style/apple-touch-icon.png';
import appLogo from '../style/app-logo.svg';

import { appConfig, Links } from './configuration';
import { Icons } from './icons';

/**
 * Creates a logo, consisting of an 'img' element wrapped inside an 'a' (anchor) element.
 *
 * @param src - The media source URL for the img element.
 * @param alt - The alt text for the img element.
 * @param href - The URL the anchor element should link to (optional).
 * @returns {HTMLAnchorElement} - The anchor element containing the logo image.
 */
export const createLogo = (
  src: string,
  alt: string,
  href?: string
): HTMLAnchorElement => {
  const logoAnchorEl = document.createElement('a');
  logoAnchorEl.href = href || '#';
  logoAnchorEl.target = '_blank';

  const logoImgEl = document.createElement('img');
  logoImgEl.src = src;
  logoImgEl.alt = alt;

  logoAnchorEl.appendChild(logoImgEl);
  return logoAnchorEl;
};

/**
 * Overrides the default document title and favicon.
 *
 * @param {string} title - The application title to set.
 * @param {string} faviconSource - The URL or path for the application favicon.
 */
export const initiAppFaviconAndTitle = (
  title: string,
  faviconSource: string
) => {
  const head = document.head;

  const iconLinks = head.querySelectorAll('link[rel="icon"]');
  const shortcutIconLinks = head.querySelectorAll('link[rel="shortcut icon"]');
  const appleTouchIconLinks = head.querySelectorAll(
    'link[rel="apple-touch-icon"]'
  );
  const busyIconLinks = head.querySelectorAll('link[type="image/x-icon"]');

  // Existent favicons set by JupyterLab
  [
    ...iconLinks,
    ...shortcutIconLinks,
    ...appleTouchIconLinks,
    ...busyIconLinks
  ].forEach(favicon => {
    if (head.contains(favicon)) {
      head.removeChild(favicon);
    }
  });

  const linkIcon = document.createElement('link');
  linkIcon.rel = 'icon';
  linkIcon.type = 'image/png';
  linkIcon.href = faviconSource;
  linkIcon.setAttribute('sizes', '32x32');
  head.appendChild(linkIcon);

  const linkShortCut = document.createElement('link');
  linkShortCut.rel = 'shortcut icon';
  linkShortCut.type = 'image/png';
  linkShortCut.href = faviconSource;
  linkShortCut.setAttribute('sizes', '32x32');
  head.appendChild(linkShortCut);

  const linkAppleTouch = document.createElement('link');
  linkAppleTouch.rel = 'apple-touch-icon';
  linkAppleTouch.href = appleTouchIcon;
  linkAppleTouch.setAttribute('sizes', '180x180');
  head.appendChild(linkAppleTouch);

  const svgDataUrl = `data:image/svg+xml;charset=utf-8,${encodeURIComponent(Icons.DespLogo)}`;
  const linkMaskIcon = document.createElement('link') as HTMLLinkElement & {
    color: string;
  };
  linkMaskIcon.rel = 'mask-icon';
  linkMaskIcon.type = 'image/svg+xml';
  linkMaskIcon.color = '#7b34db';
  linkMaskIcon.href = svgDataUrl;
  head.appendChild(linkMaskIcon);

  Object.defineProperty(document, 'title', {
    set(_arg) {
      Object.getOwnPropertyDescriptor(
        Document.prototype,
        'title'
        // Edit the document.title property setter,
        // call the original setter function for document.title and make sure 'this' is set to the document object,
        // then overrides the value to set
      )?.set?.call(document, title);
    },
    configurable: true
  });
};

/**
 * Initializes the application header by adding various elements.
 */
export const InitAppHeader = () => {
  initAppLogo();

  try {
    const userData = localStorage.getItem(
      '@jupyterlab/services:UserManager#user'
    );
    if (userData) {
      const user = JSON.parse(userData);

      if (user && user.name) {
        const headerContainerEl = document.createElement('div');
        headerContainerEl.classList.add('desp-header-container');
        headerContainerEl.id = 'desp-header-container';

        /** Create the icons */
        const iconsContainerEl = document.createElement('div');
        iconsContainerEl.classList.add('desp-header-icons');

        const icon1 = document.createElement('span');
        icon1.innerHTML = Icons.AppsIcon;
        icon1.id = 'insulaAppsMenuLinks';
        icon1.addEventListener('click', () => {
          showHeaderMenu(
            appConfig.header.insulaAppsMenuLinks,
            icon1.id as 'insulaAppsMenuLinks',
            true
          );
        });

        const icon2 = document.createElement('span');
        icon2.innerHTML = Icons.InfoIcon;
        icon2.id = 'otherInfoMenuLinks';
        icon2.addEventListener('click', () => {
          showHeaderMenu(
            appConfig.header.otherInfoMenuLinks,
            icon2.id as 'otherInfoMenuLinks',
            false
          );
        });

        iconsContainerEl.appendChild(icon1);
        iconsContainerEl.appendChild(icon2);
        headerContainerEl.appendChild(iconsContainerEl);

        /** Create the user name panel */
        const userNameContainerEl = document.createElement('div');
        userNameContainerEl.classList.add('desp-header-user');

        const iconEl = document.createElement('span');
        iconEl.innerHTML = Icons.UserIcon;

        const spanEl = document.createElement('span');
        spanEl.innerText = user.name;

        userNameContainerEl.appendChild(iconEl);
        userNameContainerEl.appendChild(spanEl);

        headerContainerEl.appendChild(userNameContainerEl);

        document.body.appendChild(headerContainerEl);
      }
    }
  } catch (error) {
    console.error('Error parsing user data:', error);
  }
};

/**
 * Adds a custom logo to the application.
 */
export const initAppLogo = () => {
  const imgEl = document.createElement('img');
  imgEl.alt = 'Destination Earth Logo';
  imgEl.src = despBanner;

  const logoSectionEL = [
    document.getElementById('jp-MainLogo'),
    document.getElementById('jp-RetroLogo')
  ];

  // Append the logo image and text to each logo section
  logoSectionEL.forEach(el => {
    if (el) {
      el.appendChild(imgEl);
      const divEl = document.createElement('div');
      divEl.classList.add('jp-MainLogo-svg');
      const svgEl = new LabIcon({ name: `Insula Code`, svgstr: appLogo });
      divEl.appendChild(svgEl.element());
      el.appendChild(divEl);
    }
  });
};

let currentOpenMenuId = '';

/**
 * Mounts or toggles the visibility of the header menu.
 *
 * @param links - The links to display in the menu.
 * @param id - An ID to identify the menu element.
 * @param avatar - If true, an avatar will be displayed next to each link.
 */
const showHeaderMenu = (
  links: Links,
  id: 'insulaAppsMenuLinks' | 'otherInfoMenuLinks',
  avatar: boolean
) => {
  const headerMenuContainerId = `desp-header-menu-container-${id}`;
  let headerMenuContainerEl = document.getElementById(headerMenuContainerId);

  // Hide the currently open menu if it's different from the one being toggled
  if (currentOpenMenuId && currentOpenMenuId !== headerMenuContainerId) {
    const currentMenuEl = document.getElementById(currentOpenMenuId);
    if (currentMenuEl) {
      currentMenuEl.style.display = 'none';
    }
  }
  if (headerMenuContainerEl) {
    // Toggle visibility of the existing menu
    if (headerMenuContainerEl.style.display === 'block') {
      headerMenuContainerEl.style.display = 'none';
      currentOpenMenuId = '';
    } else {
      headerMenuContainerEl.style.display = 'block';
      currentOpenMenuId = headerMenuContainerId;
    }
  } else {
    // Create the menu container if it doesn't exist
    headerMenuContainerEl = document.createElement('div');
    headerMenuContainerEl.id = headerMenuContainerId;
    headerMenuContainerEl.classList.add('desp-header-menu-container');

    const ulEl = document.createElement('ul');
    ulEl.classList.add('desp-footer-menu-ul');

    links.forEach(link => {
      const liEl = document.createElement('li');
      const anchorEl = document.createElement('a');
      anchorEl.href = link.href;
      anchorEl.target = '_blank';
      anchorEl.innerText = link.label;
      liEl.appendChild(anchorEl);

      if (avatar) {
        const avatarLetter = link.label.charAt(0).toUpperCase();
        const spanEl = document.createElement('div');
        spanEl.innerText = avatarLetter;
        spanEl.classList.add('desp-header-menu-avatar');
        anchorEl.before(spanEl);
      }

      ulEl.appendChild(liEl);
    });

    if (id === 'insulaAppsMenuLinks') {
      const paragraphEl = document.createElement('p');
      paragraphEl.innerText = 'Other Insula Applications';
      headerMenuContainerEl.appendChild(paragraphEl);
    }

    headerMenuContainerEl.appendChild(ulEl);
    const menuButtonEl = document.getElementById(id);

    if (id === 'insulaAppsMenuLinks' && menuButtonEl) {
      headerMenuContainerEl.style.transform = 'translateX(-50px)';
    }

    menuButtonEl?.before(headerMenuContainerEl);

    currentOpenMenuId = headerMenuContainerId;
  }
};

/**
 * Initializes the application footer with various elements.
 */
export const initAppFooter = () => {
  const footerContainerEl = document.createElement('div');
  footerContainerEl.classList.add('desp-footer-container');

  const footerWrapperEl = document.createElement('div');
  footerWrapperEl.classList.add('desp-footer-wrapper');

  footerContainerEl.appendChild(footerWrapperEl);
  footerWrapperEl.appendChild(document.createElement('div'));

  const despFooterEl = document.createElement('div');
  despFooterEl.classList.add('desp-footer');

  // Create and append the logo container
  const despLogoContainerEl = document.createElement('div');
  despLogoContainerEl.classList.add('desp-footer-logo');
  const despLogoChildEL = createLogo(despLogo, 'https://destination-earth.eu/');
  despLogoContainerEl.appendChild(despLogoChildEL);

  despFooterEl.appendChild(despLogoContainerEl);

  // Create and append the partners' logo container
  const partnersLogoContainerEl = document.createElement('div');
  partnersLogoContainerEl.classList.add('desp-footer-partners-logo');

  const logo1 = createLogo(
    destinationEarthLogo,
    'https://destination-earth.eu/'
  );
  const logo2 = createLogo(
    fundedByEULogo,
    'eu commission',
    'https://european-union.europa.eu/'
  );

  const implementedByImgEl = document.createElement('img');
  implementedByImgEl.src = implementedByLogo;
  implementedByImgEl.alt = 'Implemented by';

  const logo3 = createLogo(ecmwfLogo, 'ecmwf', 'https://www.ecmwf.int/');
  const logo4 = createLogo(esaLogo, 'esa', 'https://www.esa.int/');
  const logo5 = createLogo(
    eumetsatLogo,
    'eumetsat',
    'https://www.eumetsat.int/'
  );

  partnersLogoContainerEl.appendChild(logo1);
  partnersLogoContainerEl.appendChild(logo2);
  partnersLogoContainerEl.appendChild(implementedByImgEl);
  partnersLogoContainerEl.appendChild(logo3);
  partnersLogoContainerEl.appendChild(logo4);
  partnersLogoContainerEl.appendChild(logo5);

  despFooterEl.appendChild(partnersLogoContainerEl);

  // Create and append the menu button
  const menuButtonEL = document.createElement('div');
  menuButtonEL.id = 'desp-footer-menu-button';

  const menuButtonSpanEL = document.createElement('span');
  menuButtonSpanEL.classList.add('desp-footer-menu-button');
  menuButtonSpanEL.innerHTML = Icons.MenuIcon;

  menuButtonEL.appendChild(menuButtonSpanEL);

  menuButtonEL.addEventListener('click', () => {
    showFooterMenu(appConfig.footer.documentsMenuLinks);
  });

  despFooterEl.appendChild(menuButtonEL);
  footerWrapperEl.appendChild(despFooterEl);

  // Create and append the close button
  const closeButtonEl = document.createElement('button');
  closeButtonEl.classList.add('desp-footer-close');

  const closeSpan = document.createElement('span');
  closeSpan.innerHTML = Icons.CloseIcon;

  closeButtonEl.appendChild(closeSpan);
  footerWrapperEl.appendChild(closeButtonEl);

  closeButtonEl.addEventListener('click', () => {
    document.body.removeChild(footerContainerEl);
    showOpenFooterButton();
  });

  document.body.appendChild(footerContainerEl);
};

/**
 * Creates and displays the button to open the footer.
 */
const showOpenFooterButton = () => {
  const openButtonImgEl = document.createElement('img');
  openButtonImgEl.id = 'desp-footer-open-button';
  openButtonImgEl.src = despLogo;
  openButtonImgEl.classList.add('desp-footer-open-button');

  openButtonImgEl.addEventListener('click', () => {
    document.body.removeChild(openButtonImgEl);
    initAppFooter();
  });

  document.body.appendChild(openButtonImgEl);
};

/**
 * Toggles the visibility of the footer menu or creates it if it doesn't exist.
 *
 * @param links - The links to display in the footer menu.
 */
const showFooterMenu = (links: Links) => {
  let menuContainerEl = document.getElementById('desp-footer-menu-container');

  if (menuContainerEl) {
    if (menuContainerEl.style.display === 'none') {
      menuContainerEl.style.display = 'block';
    } else {
      menuContainerEl.style.display = 'none';
    }
  } else {
    menuContainerEl = document.createElement('div');
    menuContainerEl.id = 'desp-footer-menu-container';
    menuContainerEl.classList.add('desp-footer-menu-container');

    const ulEl = document.createElement('ul');

    links.forEach(link => {
      const liEl = document.createElement('li');
      const anchorEl = document.createElement('a');
      anchorEl.href = link.href;
      anchorEl.target = '_blank';
      anchorEl.innerText = link.label;
      liEl.appendChild(anchorEl);
      ulEl.appendChild(liEl);
    });

    menuContainerEl.appendChild(ulEl);
    const menuButtonEl = document.getElementById('desp-footer-menu-button');
    menuButtonEl?.before(menuContainerEl);
  }
};

document.addEventListener('mouseover', event => {
  const menuDivEl = document.getElementById('desp-footer-menu-container');
  if (menuDivEl && menuDivEl.style.display !== 'none') {
    if (
      !menuDivEl.contains(event.target as Node) &&
      !document
        .getElementById('desp-footer-menu-button')
        ?.contains(event.target as Node)
    ) {
      menuDivEl.style.display = 'none';
    }
  }
});

document.addEventListener('mouseover', event => {
  if (currentOpenMenuId) {
    const menuDivEl = document.getElementById(currentOpenMenuId);

    if (menuDivEl && menuDivEl.style.display !== 'none') {
      if (
        !menuDivEl.contains(event.target as Node) &&
        !document
          .getElementById('desp-header-container')
          ?.contains(event.target as Node)
      ) {
        menuDivEl.style.display = 'none';
        currentOpenMenuId = '';
      }
    }
  }
});
