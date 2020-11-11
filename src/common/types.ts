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

// Java-style functional interfaces
export type Runnable = () => void;
export type Consumer<T> = (x: T) => void;
export type Producer<T> = () => T;
export type Function<T, U> = (x: T) => U;

// Data model
export type RepoSpec = {
  title: string;
  url: string;
  description: string;
  logo: string;
};
