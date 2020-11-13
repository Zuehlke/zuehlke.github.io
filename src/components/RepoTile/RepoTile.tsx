import './RepoTile.scss';
import React from 'react';
import {RepoSpec} from "../../common/types";

type Props = {
  repo: RepoSpec
}

const RepoTile = (props: Props) => {
  return (
    <div className="RepoTile">
      <a href={props.repo.url}
         target="_blank" rel="noreferrer"
         className="content-link"
         aria-label={`${props.repo.title} repository on GitHub`}>
        <article className="repo-article">
          <h2 className="repo-name">{props.repo.title}</h2>
          <p>{props.repo.description}</p>
        </article>
      </a>
    </div>
  );
};

export default RepoTile;
