/*
pyodide-mkdocs-theme
Copyleft GNU GPLv3 🄯 2024 Frédéric Zinelli

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.
If not, see <https://www.gnu.org/licenses/>.
*/

/*
-------------------------
     GENERATED FILE
  (see mkdocs_hooks.py)
-------------------------

This module is loaded as "text/javascript", for backward compatibility, providing globals to
avoid failure of old codes.

Purposes/notes:

  - hooks files using subscribeWhenReady

  - MathJax replacements through custom_dir override. Note that, in addition to keep backward
    compatibility, loading mathjax-libs.js in a synch way also simplifies A LOT getting everything
    right at load time (because the mathjax cdn is loaded sync...)

  - The functions defined here are available in the global scope, but won't override the ones
    defined in the modules: those are explicitly imported where needed, in the modules.
    On the other hand, jsLogger becomes unusable in non modules...

  - The modules will override this globals with their own once they are loaded
*/


/**Swallow any kind of call left in a previous version of the theme, in scripts
 * loaded synchronously.
 * */
const jsLogger =()=> null
//*
globalThis.LOGGER_CONFIG = {}
/*/
globalThis.LOGGER_CONFIG = {ACTIVATE:true, all:1}
//*/



function subscribeWhenReady(waitId, callback, options={}){
    LOGGER_CONFIG.ACTIVATE && console.log('[Subscribing] (legacy) - Enter', waitId)

    if(waitId in CONFIG.subscriptionReady){
        throw new Error(`Cannot subscribe several times to "${ waitId }".`)
    }

    let {now, delay, waitFor, runOnly, maxTries} = {
        delay: 50,
        now: false,
        waitFor: null,  // or string or boolean provider
        runOnly: false,
        maxTries: 20,
        ...options
    }
    now = now && !waitFor                   // Has to wait if waitFor is used (... XD )
    CONFIG.subscriptionReady[waitId] = now

    const waitForProp = typeof (waitFor)=='string'
    const checkReady  = !waitFor    ? ()=>null
                      : waitForProp ? ()=>{ CONFIG.subscriptionReady[waitId] = $(waitFor).length > 0 }
                                    : ()=>{ CONFIG.subscriptionReady[waitId] = waitFor() }

    const isNotReady =()=>{
        checkReady()
        return !( CONFIG.subscriptionReady[waitId] && globalThis.document$ )
    }

    function autoSubscribe(){

        if(isNotReady()){
            const nTries = CONFIG.subscriptionsTries[waitId]+1 || 1
            if(nTries > maxTries){
                throw new Error(`Impossible to subscribe to ${ waitId } in time: too many tries.`)
            }
            CONFIG.subscriptionsTries[waitId] = nTries
            setTimeout(autoSubscribe, delay)

        }else{
            LOGGER_CONFIG.ACTIVATE && console.log('[Subscribing] (legacy) -', waitId)
            const wrapper=function(){
                try{
                    callback()
                }catch(e){
                    console.error(e)
                }
            }
            if(runOnly){
                wrapper()
            }else{
                const subscript = document$.subscribe(wrapper)
                document.addEventListener(CONFIG.onDoneEvent, function(){
                    LOGGER_CONFIG.ACTIVATE && console.log('[Unsubscribing] (legacy) -', waitId)
                    subscript.unsubscribe()
                })
            }
        }
    }
    autoSubscribe()

    if(!now){
        return ()=>{ CONFIG.subscriptionReady[waitId]=true }
    }
}
// TOKEN: end subscribeWhenReady
