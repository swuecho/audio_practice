interface Parameter {
        name: string,
        description: string | null,
        value: string
}

interface Hardware {
        upc: string,

        //
        os: string,
        os_generation: string,
        os_version: string,

        //
        cpu_brand: string,
        cpu_serial: string, // N5051
        cpu_model: string,

        // 
        mem_slot_type: string,
        mem_total_size: string,
        mem_type: string,
        mem_size_by_slot: string,
        
        disk_total_size: string,
        disk_slot_type: string,


        //
        screen: string // 21,24,27
}