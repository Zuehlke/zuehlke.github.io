export type NavLinkSpec = {
  href: string;
  display: string;
};

const navLinks = {
  /* Main page navigation */
  main: [
    {href: "/contributions", display: "Contributions"},
    {href: "/people", display: "People"}
  ] as NavLinkSpec[],

  /* Meta-navigation, external links */
  meta: [
    {href: "https://www.zuehlke.com", display: "Zühlke Website"},
    {href: "https://www.zuehlke.com/careers", display: "Careers"},
    {href: "https://www.zuehlke.com/insights", display: "Insights"}
  ] as NavLinkSpec[]
};

export default navLinks;
