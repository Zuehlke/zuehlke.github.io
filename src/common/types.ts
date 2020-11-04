import {ReactNode} from "react";

export type RouteSpec = {
  to: string,
  component: ReactNode,
  display: string;
};

export type MetaLinkSpec = {
  href: string;
  display: string;
};
