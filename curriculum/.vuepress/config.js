var getChildren = require("./childscript");

module.exports = {
  title: "REST APIs with Flask and Python",
  description: "The complete course notes and guide.",
  themeConfig: {
    nav: [
      { text: "Home", link: "/" },
      {
        text: "Get the course",
        link: "https://www.udemy.com/course/rest-api-flask-and-python/?referralCode=04E9923849AD8B30AB4A",
      },
    ],
    sidebar: [
      {
        title: "Start here",
        path: "/",
      },
      {
        title: "Section 1: Welcome to the Course",
        path: "/section01/",
        children: getChildren("section01", "lectures"),
      },
      {
        title: "Section 2: Python Refresher",
        path: "/section02/",
      },
      {
        title: "Section 3: Your first REST API",
        path: "/section03/",
        children: getChildren("section03", "lectures"),
      },
    ],
    sidebarDepth: 0,
  },
  markdown: {
    extendMarkdown: (md) => {
      md.use(require("markdown-it-footnote"));
    },
  },
  plugins: [["plausible", { domain: "rest-apis.teclado.com" }]],
};
