import './Contributions.scss';
import React from 'react';
import RepoTile from "../../components/RepoTile/RepoTile";
import TileGrid from "../../components/TileGrid/TileGrid";
import {RepoSpec} from "../../common/types";

type Props = {
  repos: RepoSpec[]
}

const Contributions = (props: Props) => {

  return (
    <div className="Contributions">
      <div className="container">
        <h1 className="title">Contributions</h1>
        <TileGrid>
          {props.repos.map((repo: RepoSpec) => <RepoTile key={repo.url} repo={repo}/>)}
        </TileGrid>
      </div>
    </div>
  );
};

export default Contributions;
