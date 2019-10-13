module.exports = {
  title: "Hypothesis-Bio",
  description: "Just playing around",
  base: "/hypothesis-bio/",
  plugins: ["@vuepress/last-updated", "@vuepress/active-header-links"],
  themeConfig: {
    sidebar: "auto",
    activeHeaderLinks: true,
    nav: [
      { text: "Home", link: "/" },
      { text: "Contribute", link: "/contributing" },
      { text: "API Reference", link: "/api" },
      { text: "GitHub", link: "https://github.com/Lab41/hypothesis-bio" }
    ]
  }
}
