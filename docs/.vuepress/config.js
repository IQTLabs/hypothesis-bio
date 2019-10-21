module.exports = {
  title: "Hypothesis-Bio",
  description: "Property-Based Testing for Biology",
  base: "/hypothesis-bio/",
  plugins: ["@vuepress/last-updated"],
  themeConfig: {
    displayAllHeaders: true,
    sidebar: [
      "/",
      "/guide",
      "/contributing",
      {
        title: "API Reference",
        collapsable: false,
        children: [
          "/api/blast6",
          "/api/fasta",
          "/api/fastq",
          "/api/sequence_identifiers",
          "/api/sequences"
        ]
      }
    ],
    repo: "Lab41/hypothesis-bio",
    smoothScroll: true,
    nav: [
      {
        text: "Hypothesis Docs",
        link: "https://hypothesis.readthedocs.io/en/latest/"
      },
      {
        text: "Get Help",
        link: "https://github.com/Lab41/hypothesis-bio/issues/new"
      }
    ]
  }
}
