export type RepoSpec = {
  id: number;
  name: string;
  owner: {
    login: string;
    id: number;
  };
  html_url: string;
  created_at: string;
  stargazers_count: number;
  watchers_count: number;
  forks_count: number;
  fork: boolean;
  language: string | null;
}

export type PersonSpec = {
  id: number;
  login: string;
  name: string | null;
  bio: string | null;
  avatar_url: string;
  html_url: string;
}
