import './Contributions.scss';
import React, {useState} from 'react';
import RepoTile from "../../components/RepoTile/RepoTile";
import TileGrid from "../../components/TileGrid/TileGrid";
import {RepoModel} from "../../common/model";
import SearchBar from "../../components/SearchBar/SearchBar";

type Props = {
  repos: RepoModel[]
  externalRepos: RepoModel[];
  displayedRepos: RepoModel[];
}

const byText = (text: string) =>  (repo: RepoModel) => repo.name.toUpperCase().includes(text.toUpperCase())
    || repo.description?.toUpperCase().includes(text.toUpperCase())

const byStargazersCount = (a: RepoModel, b: RepoModel) => b.stargazers_count - a.stargazers_count;

const Contributions = (props: Props) => {

  const [displayedRepos, setDisplayedRepos] = useState(props.displayedRepos);

  const searchContributions = (text: string) => {
    setDisplayedRepos(
        props.repos.concat(props.externalRepos)
        .filter(byText(text))
        .sort(byStargazersCount)
    );
  };

  return (
      <div className="Contributions">
        <div className="container">
          <h1 className="title">Contributions</h1>
          <div className="search-bar-container">
            <div className={'search-bar'}>
              <SearchBar placeholder={'Search contributions...'} onChangeText={searchContributions}/>
            </div>
          </div>
          <TileGrid>
            {displayedRepos.map((repo: RepoModel) => <RepoTile key={repo.html_url} repo={repo}/>)}
          </TileGrid>
        </div>
      </div>
  );
};

export default Contributions;
