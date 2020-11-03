export type NavLinkSpec = {
  target: string;
  value: string;
};

const navLinks = {
  /* Main page navigation */
  main: [
    {target: "/contributions", value: "Contributions"},
    {target: "/people", value: "People"}
  ] as NavLinkSpec[],

  /* Meta-navigation, external links */
  meta: [
    {target: "https://www.zuehlke.com", value: "Zühlke Website"},
    {target: "https://www.zuehlke.com/careers", value: "Careers"},
    {target: "https://www.zuehlke.com/insights", value: "Insights"}
  ] as NavLinkSpec[]
};

export default navLinks;
