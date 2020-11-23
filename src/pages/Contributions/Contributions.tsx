import './Contributions.scss';
import React from 'react';
import RepoTile from "../../components/RepoTile/RepoTile";
import TileGrid from "../../components/TileGrid/TileGrid";
import {RepoModel} from "../../common/model";

type Props = {
  repos: RepoModel[]
}

const Contributions = (props: Props) => {



  return (
    <div className="Contributions">
      <div className="container">
        <h1 className="title">Contributions</h1>
        <TileGrid>
          {props.repos.map((repo: RepoModel) => <RepoTile key={repo.html_url} repo={repo}/>)}
        </TileGrid>
      </div>
    </div>
  );
};

export default Contributions;
