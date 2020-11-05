import './TileGrid.scss';
import React from 'react';

type Props = {}

const TileGrid = (props: Props) => {

  const numTiles = 10;
  const tiles = Array.from(Array(numTiles).keys()).map((idx) => `Repo ${idx+1}`);

  const tile = (text: string) => {
    return (
      <div className="grid-cell">
        <div className="grid-cell-inner">
          <div className="tile">
            <span>{text}</span>
          </div>
        </div>
      </div>
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
