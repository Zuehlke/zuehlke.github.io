import './PersonTile.scss';
import React from 'react';
import {PersonSpec} from "../../common/model";

type Props = {
  person: PersonSpec;
}

const PersonTile = (props: Props) => {
  return (
    <div className="PersonTile">
      <a href={props.person.html_url} target="_blank" rel="noreferrer"
         aria-label={`GitHub profile ${props.person.login}`}>
        <article className="person-article">
          <div className="profile-container">
            <img src={props.person.avatar_url} className="avatar" alt={`Avatar ${props.person.login}`}/>
            <h2 className="github-login profile-text">{props.person.login}</h2>
            <h3 className="full-name text">{props.person.name}</h3>
          </div>
          <div className="description-container">
            <p className="description">{props.person.bio}</p>
          </div>
        </article>
      </a>
    </div>
  );
};

export default PersonTile;
