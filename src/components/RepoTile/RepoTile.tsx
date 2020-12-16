import './RepoTile.scss';
import React from 'react';
import {RepoModel} from "../../common/model";

type Props = {
  repo: RepoModel
}

const RepoTile = (props: Props) => {
  return (
    <div className="RepoTile">
      <a href={props.repo.html_url}
         target="_blank" rel="noreferrer"
         className="content-link"
         aria-label={`${props.repo.name} repository on GitHub`}>
        <article className="repo-article">
          <h2 className="repo-name">{props.repo.name}</h2>
          <p>{props.repo.description}</p>
        </article>
      </a>
    </div>
  );
};

export default RepoTile;
