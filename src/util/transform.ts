#!/usr/bin/env node
/*
* Mbed Linux CLI
* Copyright ARM Limited 2017
*
* Licensed under the Apache License, Version 2.0 (the "License");
* you may not use this file except in compliance with the License.
* You may obtain a copy of the License at
*
* http://www.apache.org/licenses/LICENSE-2.0
*
* Unless required by applicable law or agreed to in writing, software
* distributed under the License is distributed on an "AS IS" BASIS,
* WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
* See the License for the specific language governing permissions and
* limitations under the License.
*/

import { Transform } from "stream";

export const prettifyStream = new Transform({
    transform(chunk: any, encoding: any, callback: any) {
        if (encoding !== "buffer") {
            return callback(null, chunk.toString(encoding));
        }

        const chunkStr: string = chunk.toString();
        if (chunkStr) {
            chunkStr.split("\n").forEach(strObj => {
                if (!strObj) { return null; }
                const { stream = "" } = JSON.parse(strObj);
                this.push(stream);
            });
        }

        callback();
    }
});
