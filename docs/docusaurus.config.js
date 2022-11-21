// @ts-check
// Note: type annotations allow type checking and IDEs autocompletion

const lightCodeTheme = require("prism-react-renderer/themes/okaidia");
const darkCodeTheme = require("prism-react-renderer/themes/dracula");

/** @type {import('@docusaurus/types').Config} */
const config = {
  title: "REST APIs with Flask and Python",
  tagline: "Build and deploy REST APIs using Flask, PostgreSQL, and Docker",
  url: "https://rest-apis-flask.teclado.com",
  baseUrl: "/",
  onBrokenLinks: "throw",
  onBrokenMarkdownLinks: "warn",
  favicon: "img/favicon.ico",
  organizationName: "tecladocode", // Usually your GitHub org/user name.
  projectName: "rest-apis-flask-python", // Usually your repo name.
  scripts: [
    {
      src: "https://plau-prox.teclado.workers.dev/get/script.outbound-links.js",
      defer: true,
      "data-domain": "rest-apis-flask.teclado.com",
      "data-api": "https://plau-prox.teclado.workers.dev/send/event",
    },
  ],
  presets: [
    [
      "@docusaurus/preset-classic",
      /** @type {import('@docusaurus/preset-classic').Options} */
      ({
        docs: {
          sidebarPath: require.resolve("./sidebars.js"),
          exclude: ["**/start/**", "**/end/**"],
          // Please change this to your repo.
          editUrl:
            "https://github.com/tecladocode/rest-apis-flask-python/tree/develop/docs/",
        },
        theme: {
          customCss: require.resolve("./src/css/custom.css"),
        },
      }),
    ],
  ],
  themeConfig:
    /** @type {import('@docusaurus/preset-classic').ThemeConfig} */
    ({
      docs: {
        sidebar: {
          hideable: true,
        },
      },
      algolia: {
        // The application ID provided by Algolia
        appId: "1BEGBIP9SH",

        // Public API key: it is safe to commit it
        apiKey: "882167549d623413f9b5314788a0d900",

        indexName: "docusaurus-2",

        // Optional: see doc section below
        // contextualSearch: true,

        // Optional: Specify domains where the navigation should occur through window.location instead on history.push. Useful when our Algolia config crawls multiple documentation sites and we want to navigate with window.location.href to them.
        // externalUrlRegex: "external\\.com|domain\\.com",

        // Optional: Algolia search parameters
        searchParameters: {},

        // Optional: path for search page that enabled by default (`false` to disable it)
        searchPagePath: "search",
      },
      navbar: {
        title: "REST APIs with Flask and Python",
        logo: {
          alt: "Teclado Logo",
          src: "img/favicon.ico",
        },
        items: [
          {
            type: "doc",
            docId: "course_intro/intro",
            position: "left",
            label: "Tutorial",
          },
          {
            href: "/insomnia-files/",
            position: "left",
            label: "Insomnia files",
          },
          {
            href: "https://go.tecla.do/rest-apis-ebook",
            label: "Get the course",
            position: "right",
          },
        ],
      },
      announcementBar: {
        id: "support_us",
        content:
          '<span style="font-weight: 600">Unlock all video lessons and support us by <a target="_blank" style="background-image: linear-gradient(90deg, #FF7D82, #50e3c2); background-clip: text; color: transparent; " rel="noopener noreferrer" href="https://go.tecla.do/rest-apis-ebook">buying the course</a>!</span>',
        backgroundColor: "#1c2023",
        textColor: "#fff",
        isCloseable: false,
      },
      footer: {
        style: "dark",
        links: [
          {
            title: "Learn",
            items: [
              {
                href: "https://go.tecla.do/rest-apis-ebook",
                label: "Get the course",
              },
              {
                label: "Tutorial",
                to: "/docs/course_intro/",
              },
            ],
          },
          {
            title: "Social",
            items: [
              {
                label: "Discord",
                href: "https://go.tecla.do/discord",
              },
              {
                label: "Twitter",
                href: "https://twitter.com/jslvtr",
              },
            ],
          },
          {
            title: "More",
            items: [
              {
                label: "GitHub",
                href: "https://github.com/tecladocode/rest-apis-flask-python",
              },
            ],
          },
        ],
        copyright: `Copyright © ${new Date().getFullYear()} Teclado Ltd. Built with Docusaurus.`,
      },
      prism: {
        theme: lightCodeTheme,
        darkTheme: darkCodeTheme,
        additionalLanguages: ["docker"],
      },
    }),
};

module.exports = config;
