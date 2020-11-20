import './RepoTile.scss';
import React from 'react';
import {RepoSpec} from "../../common/model";

type Props = {
  repo: RepoSpec
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
          { /* TODO: <p>{props.repo.description}</p>*/ }
        </article>
      </a>
    </div>
  );
};

export default RepoTile;
