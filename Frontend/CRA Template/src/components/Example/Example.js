import './Example.css';
import sample from './assets/sample.png';
export default function Example() {
  return (
    <div className='exampleClass'>
      <h1>Example</h1>
      <img src={sample} alt='sample' />
    </div>
  );
}