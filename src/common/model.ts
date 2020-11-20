export type RepoSpec = {
  id: number;
  name: string;
  owner: {
    login: string;
    id: number;
  };
  html_url: string;
  created_at: string;
  stargazers_count: string;
  watchers_count: string;
  forks_count: string;
  fork: boolean;
  language: string;
}

export type PersonSpec = {
  id: number;
  login: string;
  name: string;
  bio: string;
  avatar_url: string;
  html_url: string;
}
