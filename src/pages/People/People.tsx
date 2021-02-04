import './People.scss';
import React, {useState} from 'react';
import TileGrid from "../../components/TileGrid/TileGrid";
import {PersonModel} from "../../common/model";
import PersonTile from "../../components/PersonTile/PersonTile";
import SearchBar from "../../components/SearchBar/SearchBar";

type Props = {
  people: PersonModel[]
  displayedPeople: PersonModel[];
}

const byText = (text: string) =>  (person: PersonModel) => person.login.toUpperCase().includes(text.toUpperCase())
    || (person.name && person.name.toUpperCase().includes(text.toUpperCase()))
    || person.bio?.toUpperCase().includes(text.toUpperCase());

const People = (props: Props) => {

  const [displayedPeople, setDisplayedPeople] = useState(props.displayedPeople);

  const searchPeople = (text: string) => {
    setDisplayedPeople(props.people.filter(byText(text)));
  };

  return (
    <div className="People">
      <div className="Contributions">
        <div className="container">
          <h1 className="title">People</h1>
          <div className="search-bar-container">
            <div className={'search-bar'}>
              <SearchBar placeholder={'Search people...'} onChangeText={searchPeople}/>
            </div>
          </div>
          <TileGrid>
            {displayedPeople.map((person: PersonModel) => <PersonTile key={person.html_url} person={person}/>)}
          </TileGrid>
        </div>
      </div>
    </div>
  );
};

export default People;
