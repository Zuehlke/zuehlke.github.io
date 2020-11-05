import './TileGrid.scss';
import React from 'react';

type Props = {}

const TileGrid = (props: Props) => {
  return (
    <div className="TileGrid">
      <div className="content">
        <div className="tile">Repo 1</div>
        <div className="tile">Repo 2</div>
        <div className="tile">Repo 3</div>
        <div className="tile">Repo 4</div>
        <div className="tile">Repo 5</div>
      </div>
    </div>
  );
};

export default TileGrid;
