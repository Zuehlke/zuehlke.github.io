import './PersonTile.scss';
import React from 'react';
import {PersonSpec} from "../../common/types";

type Props = {
  person: PersonSpec;
}

const PersonTile = (props: Props) => {
  return (
    <div className="PersonTile">
      <div className="profile-container">
        <img src={props.person.logoUrl} className="avatar" alt={`Avatar ${props.person.title}`}/>
        <span className="title">{props.person.title}</span>
        <span>{props.person.name}</span>
      </div>
      <div className="description-container">
        {props.person.description}
      </div>
    </div>
  );
};

export default PersonTile;
