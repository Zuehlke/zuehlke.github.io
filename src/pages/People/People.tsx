import './People.scss';
import React from 'react';
import TileGrid from "../../components/TileGrid/TileGrid";
import {PersonModel} from "../../common/model";
import PersonTile from "../../components/PersonTile/PersonTile";

type Props = {
  people: PersonModel[]
}

const People = (props: Props) => {
  return (
    <div className="People">
      <div className="Contributions">
        <div className="container">
          <h1 className="title">People</h1>
          <TileGrid>
            {props.people.map((person: PersonModel) => <PersonTile key={person.html_url} person={person}/>)}
          </TileGrid>
        </div>
      </div>
    </div>
  );
};

export default People;
