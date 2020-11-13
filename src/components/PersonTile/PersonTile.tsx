import './PersonTile.scss';
import React from 'react';
import {PersonSpec} from "../../common/types";

type Props = {
  person: PersonSpec;
}

const PersonTile = (props: Props) => {
  return (
    <div className="PersonTile">
      <a href={props.person.url} target="_blank" rel="noreferrer" aria-label={`GitHub profile ${props.person.title}`}>
        <article className="person-article">
          <div className="profile-container">
            <img src={props.person.logoUrl} className="avatar" alt={`Avatar ${props.person.title}`}/>
            <h2 className="github-login profile-text">{props.person.title}</h2>
            <h3 className="full-name text">{props.person.name}</h3>
          </div>
          <div className="description-container">
            <p className="description">{props.person.description}</p>
          </div>
        </article>
      </a>
    </div>
  );
};

export default PersonTile;
