// Regression test: a record created during Fetch must remain pending.
const vm = require('node:vm');
const fs = require('node:fs');
const assert = require('node:assert/strict');
const source = fs.readFileSync('public/app.js','utf8');
const syncCode = source.slice(source.indexOf('let syncing ='),source.indexOf('async function confirmActivity'));
const stores={students:[{id:'student-original',synced:false}],activities:[],deletions:[]};
let finishFetch, calls=0;
const ctx=vm.createContext({navigator:{onLine:true}, $:()=>({textContent:''}),
  AbortSignal,console,serverAvailable:null,
  readAll:async name=>structuredClone(stores[name]),
  put:async(name,item)=>{const i=stores[name].findIndex(x=>x.id===item.id);if(i<0)stores[name].push(item);else stores[name][i]=item;},
  remove:async(name,id)=>{stores[name]=stores[name].filter(x=>x.id!==id);},
  reload:async()=>{},updateConnection:()=>{},
  fetch:async()=>{calls++;await new Promise(resolve=>finishFetch=resolve);return {ok:true,json:async()=>({students:[{id:'student-original'}],activities:[]})};}
});
vm.runInContext(syncCode,ctx);
(async()=>{
  const running=vm.runInContext('sync()',ctx);
  while(!finishFetch)await new Promise(resolve=>setImmediate(resolve));
  stores.students.push({id:'student-created-during-fetch',synced:false});
  finishFetch();await running;
  assert.equal(stores.students[0].synced,true);
  assert.equal(stores.students[1].synced,false);
  assert.equal(calls,1);
  ctx.fetch=async()=>{throw Error('offline');};
  await vm.runInContext('sync()',ctx);
  assert.equal(stores.students[1].synced,false);
  assert.equal(ctx.serverAvailable,false);
  console.log('OK: concurrent record remains pending; network failure preserves local data.');
})().catch(error=>{console.error(error);process.exitCode=1;});
