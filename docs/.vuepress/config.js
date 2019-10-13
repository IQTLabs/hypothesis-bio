module.exports = {
  title: "Hypothesis-Bio",
  description: "Property-Based Testing for Biology",
  base: "/hypothesis-bio/",
  plugins: ["@vuepress/last-updated"],
  themeConfig: {
    sidebar: "auto",
    repo: "Lab41/hypothesis-bio",
    smoothScroll: true,
    nav: [
      { text: "Home", link: "/" },
      { text: "Contribute", link: "/contributing" },
      { text: "API Reference", link: "/api" }
    ]
  }
}
