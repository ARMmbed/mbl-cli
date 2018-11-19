/*
* Mbed Linux OS CLI
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

import { DeviceCommand } from "../../../deviceCommand";
import { log } from "../../../utils/logger";

export const command = "restart [address]";
export const describe = "Restart the application";

export const builder: DeviceCommand = {
    address: {
        description: "address of the device"
    }
};

export function handler(args: DeviceCommand) {
    log(`command not implemented ${JSON.stringify(args)}`);
}
