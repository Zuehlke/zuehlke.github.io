import './RepoTile.scss';
import React from 'react';
import {RepoSpec} from "../../common/types";

type Props = {
  repo: RepoSpec
}

const RepoTile = (props: Props) => {
  return (
    <div className="RepoTile">
      <a href={props.repo.url} target="_blank" rel="noreferrer" className="content-link">
        <h2 className="title">{props.repo.title}</h2>
        <article className="description">
          {props.repo.description}
        </article>
      </a>
    </div>
  );
};

export default RepoTile;
