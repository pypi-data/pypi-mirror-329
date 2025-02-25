echo "###################"
echo "## Building Dist ##"
echo "###################"
cd website_src/third_party

echo "== Cleaning prior =="
rm -r pyodide
rm -r pyscript
rm -r pyscript-offline

mkdir -p pyscript-offline

echo "== Building =="
cd pyscript-offline/

echo "-- Building pyscript --"
echo '{}' > ./package.json
npm i @pyscript/core@0.6.20
mkdir -p public
cp -R ./node_modules/@pyscript/core/dist ./public/pyscript

echo "-- Building Pyodide --"
npm i pyodide
mkdir -p ./public/pyodide
cp ./node_modules/pyodide/pyodide* ./public/pyodide/
cp ./node_modules/pyodide/python_stdlib.zip ./public/pyodide/

echo "-- Getting Pyodide dist --"


cd ..

echo "== Creating dist =="
mkdir pyodide
mkdir pyscript

echo "-- Dist pyodide --"
wget https://cdn.jsdelivr.net/pyodide/v0.26.3/full/pyodide-lock.json
mv pyodide-lock.json pyodide

wget https://cdn.jsdelivr.net/pyodide/v0.26.3/full/pyodide.asm.js
mv pyodide.asm.js pyodide

wget https://cdn.jsdelivr.net/pyodide/v0.26.3/full/pyodide.asm.wasm
mv pyodide.asm.wasm pyodide

wget https://cdn.jsdelivr.net/pyodide/v0.26.3/full/pyodide.mjs
mv pyodide.mjs pyodide

wget https://cdn.jsdelivr.net/pyodide/v0.26.3/full/python_stdlib.zip
mv python_stdlib.zip pyodide

wget https://cdn.jsdelivr.net/pyodide/v0.26.3/full/micropip-0.6.0-py3-none-any.whl
mv micropip-0.6.0-py3-none-any.whl pyodide

wget https://cdn.jsdelivr.net/pyodide/v0.26.3/full/packaging-23.2-py3-none-any.whl
mv packaging-23.2-py3-none-any.whl pyodide

echo "-- Dist pyscript --"
cp pyscript-offline/public/pyscript/core.css pyscript
cp pyscript-offline/public/pyscript/core.js pyscript
cp pyscript-offline/public/pyscript/core-*.js pyscript
cp pyscript-offline/public/pyscript/error-*.js pyscript
cp pyscript-offline/public/pyscript/py-terminal-*.js pyscript
cp pyscript-offline/public/pyscript/toml-*.js pyscript

echo "-- Dist pyscript deps --"
cp pyscript-offline/public/pyscript/deprecations-manager-*.js pyscript
cp pyscript-offline/public/pyscript/donkey-*.js pyscript
cp pyscript-offline/public/pyscript/py-editor-*.js pyscript
cp pyscript-offline/public/pyscript/py-game-*.js pyscript

echo "== Clean up =="
rm -r pyscript-offline
cd ../..

echo "################"
echo "## Update Web ##"
echo "################"
bash support/render_website.sh

echo "###################"
echo "## Update Editor ##"
echo "###################"
cp -r website_src/third_party/pyodide editor_src/third_party/pyodide
cp -r website_src/third_party/pyscript editor_src/third_party/pyscript
rm -r editor_src/dist
mkdir editor_src/dist
echo "Directory containing runtime distribution." > editor_src/dist/ABOUT.txt
cp website_build/dist/sketchingpy-*.whl editor_src/dist
