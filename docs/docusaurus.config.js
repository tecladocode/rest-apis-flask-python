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
      src: "https://plausible.io/js/plausible.js",
      defer: true,
      "data-domain": "rest-apis-flask.teclado.com",
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
          editUrl: "https://github.com/tecladocode/rest-apis-flask-python/",
        },
        theme: {
          customCss: require.resolve("./src/css/custom.css"),
        },
      }),
    ],
  ],
  plugins: [require.resolve("@cmfcmf/docusaurus-search-local")],
  themeConfig:
    /** @type {import('@docusaurus/preset-classic').ThemeConfig} */
    ({
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
            href: "https://go.tecla.do/rest-apis-sale",
            label: "Get the course",
            position: "right",
          },
        ],
      },
      footer: {
        style: "dark",
        links: [
          {
            title: "Learn",
            items: [
              {
                href: "https://go.tecla.do/rest-apis-sale",
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
