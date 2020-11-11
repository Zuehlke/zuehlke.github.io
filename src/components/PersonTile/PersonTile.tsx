import './PersonTile.scss';
import React from 'react';
import {PersonSpec} from "../../common/types";

type Props = {
  person: PersonSpec;
}

const PersonTile = (props: Props) => {
  return (
    <div className="PersonTile">
      <a href={props.person.url} target="_blank" rel="noreferrer">
        <div className="profile-container">
          <img src={props.person.logoUrl} className="avatar" alt={`Avatar ${props.person.title}`}/>
          <span className="title text">{props.person.title}</span>
          <span className="name text">{props.person.name}</span>
        </div>
        <div className="description-container">
          <span className="description">{props.person.description}</span>
        </div>
      </a>
    </div>
  );
};

export default PersonTile;
