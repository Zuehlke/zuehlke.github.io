import './RepoTile.scss';
import React from 'react';
import {RepoModel} from "../../common/model";
import {FontAwesomeIcon} from '@fortawesome/react-fontawesome';
import {faCodeBranch, faEye, faStar} from "@fortawesome/free-solid-svg-icons";

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
        <div className={"repo-icons"}>
          <div className={"repo-icon"}>
            <FontAwesomeIcon style={{marginRight: '0.5em'}} title="Stargazers" icon={faStar}/>
            {props.repo.stargazers_count}
          </div>
          <div className={"repo-icon"}>
            <FontAwesomeIcon style={{marginRight: '0.5em'}} title="Forks" icon={faCodeBranch}/>
            {props.repo.forks_count}
          </div>
          <div className={"repo-icon"}>
            <FontAwesomeIcon style={{marginRight: '0.5em'}} title="Watchers" icon={faEye}/>
            {props.repo.watchers_count}
          </div>
        </div>
      </a>
    </div>
  );
};

export default RepoTile;
