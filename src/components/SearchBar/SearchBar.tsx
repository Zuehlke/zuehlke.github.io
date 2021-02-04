import './SearchBar.scss';
import React, {ChangeEvent} from 'react';

type Props = {
  onChangeText?: (text: string) => any
  placeholder?: string
}

const SearchBar = (props: Props) => {

  const _onChange = (event: ChangeEvent<HTMLInputElement>) => {
    const value = event.target.value;
    props.onChangeText && props.onChangeText(value);
  };

  return (
      <div>
        <div className="SearchBar">
          <input type={'search'} placeholder={props.placeholder} onChange={_onChange}/>
        </div>
      </div>
  )
}

SearchBar.defaultProps = {value: '', placeholder: 'Search...'} as Partial<Props>

export default SearchBar;
