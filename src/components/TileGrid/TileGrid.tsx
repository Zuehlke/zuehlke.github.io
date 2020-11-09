import './TileGrid.scss';
import React from 'react';

type Props = {}

const TileGrid = (props: Props) => {

  const numTiles = 10;
  const tiles = Array.from(Array(numTiles).keys()).map((idx) => `Repo ${idx+1}`);

  const tile = (text: string) => {
    return (
      <a className="grid-cell" href="http://www.zuehlke.com" target="_blank" rel="noreferrer">
        <div className="grid-cell-inner">
          <div className="tile">
            <span>{text}</span>
          </div>
        </div>
      </a>
    );
  }

  return (
    <div className="TileGrid">
      <div className="grid">
        {tiles.map((text: string) => tile(text))}
      </div>
    </div>
  );
};

export default TileGrid;
