module.exports = {
  title: "Hypothesis-Bio",
  description: "Property-Based Testing for Biology",
  base: "/hypothesis-bio/",
  plugins: ["@vuepress/last-updated"],
  themeConfig: {
    sidebar: "auto",
    smoothScroll: true,
    nav: [
      { text: "Home", link: "/" },
      { text: "Contribute", link: "/contributing" },
      { text: "API Reference", link: "/api" },
      { text: "GitHub", link: "https://github.com/Lab41/hypothesis-bio" }
    ]
  }
}
